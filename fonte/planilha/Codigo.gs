/**
 * Me chame de majestade: recebe o progresso da Karina e grava na planilha.
 * Cole este código em Extensões > Apps Script da planilha "Progresso Karina"
 * e publique como app da Web (Executar como: eu; Quem pode acessar: qualquer pessoa).
 * O script só ACRESCENTA linhas. Ele não devolve nenhum dado a quem chama.
 */
const ABA = 'respostas';
const CAB = ['chave','recebido_em','respondido_em','dispositivo','round','modo','codigo','qid',
             'materia','item','nivel','origem','tema','marcou','gabarito','acertou'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const dados = JSON.parse(e.postData.contents);
    if (dados.app !== 'majestade' || !Array.isArray(dados.eventos)) return resposta({ok:false});
    const planilha = SpreadsheetApp.getActiveSpreadsheet();
    let aba = planilha.getSheetByName(ABA);
    if (!aba) { aba = planilha.insertSheet(ABA); aba.appendRow(CAB); aba.setFrozenRows(1); }
    const n = aba.getLastRow();
    const ja = new Set(n > 1 ? aba.getRange(2, 1, n - 1, 1).getValues().map(l => String(l[0])) : []);
    const agora = new Date();
    const linhas = [];
    dados.eventos.slice(0, 500).forEach(ev => {
      const k = String(ev.chave || '').slice(0, 80);
      if (!k || ja.has(k)) return;
      ja.add(k);
      linhas.push([k, agora, ev.quando, String(dados.disp || '').slice(0, 20), ev.round, ev.modo, ev.cod, ev.qid,
                   ev.materia || ev.disc, ev.item, ev.nivel, ev.origem, ev.tema, ev.marcou, ev.gabarito, ev.acertou]
                  .map(v => (typeof v === 'string' ? v.slice(0, 300) : v)));
    });
    if (linhas.length) aba.getRange(aba.getLastRow() + 1, 1, linhas.length, CAB.length).setValues(linhas);
    return resposta({ok:true, gravadas: linhas.length});
  } catch (err) {
    return resposta({ok:false});
  } finally {
    lock.releaseLock();
  }
}

function doGet() { return resposta({ok:true}); }

function resposta(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
