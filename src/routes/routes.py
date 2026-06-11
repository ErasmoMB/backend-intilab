from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from src.services.investigador_service import investigador_service
from src.utils.logger import logger
from src.utils.exceptions import APIException

router = APIRouter()

@router.get('/datos')
async def datos_investigadores():
    try:
        return investigador_service.obtener_todos()
    except Exception as e:
        logger.error(f"Error en datos_investigadores: {e}")
        raise APIException("Error interno del servidor", 500)

@router.get('/health')
async def health_check():
    return {"status": "healthy"}

@router.get('/diagnostico', response_class=HTMLResponse)
async def diagnostico():
    return HTMLResponse(content="""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Diagnóstico Scopus</title>
<style>
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;margin:20px;background:#f5f5f5}
  h1{color:#333}
  button{padding:10px 24px;font-size:1rem;cursor:pointer;background:#007bff;color:#fff;border:none;border-radius:6px}
  button:disabled{background:#6c757d;cursor:not-allowed}
  #status{font-size:.9rem;color:#666;margin-left:12px}
  table{border-collapse:collapse;width:100%;margin-top:16px;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.1);font-size:.8rem}
  th,td{padding:6px 10px;text-align:left;border-bottom:1px solid #eee}
  th{background:#007bff;color:#fff}
  .ok{color:#28a745;font-weight:700}
  .err{color:#dc3545;font-weight:700}
  .zero{color:#e67e22;font-weight:700}
  .total-row{background:#e8f4f8;font-weight:700}
</style>
</head>
<body>
<h1>Diagnóstico Scopus</h1>
<button id="btnRun" onclick="run()">Ejecutar diagnóstico</button>
<span id="status">Listo</span>
<div id="output"></div>
<script>
const IDS=[
  ["57210377414","Enrique Lee Huaman\u00ed"],["57225097710","Sebastian J. Ramos-Cosi"],
  ["57203357446","Victor Romero-Alva"],["58562875900","Guillermo Segundo Mi\u00f1an-Olivos"],
  ["57205596738","Alicia Alva-Mantari"],["56741286500","Natalia I. Vargas-Cuentas"],
  ["57215928001","Juan Morales"],["57215218631","Celia Bertha Vargas-De-La-Cruz"],
  ["58127854500","Daniel E. Yupanqui-Lorenzo"],["57223372908","Tania Arauco-Lozada"],
  ["15750919900","Telmo A. Mej\u00eda-Garc\u00eda"],["57209658640","Ivan Iraola-Real"],
  ["57205765369","Milton Alexis Gonzales-Macavilca"],["57364197600","Zulema Daria Leiva-Baz\u00e1n"],
  ["58886913200","(desconocido)"],["57930813500","Linett Velasquez-Jimenez"],
  ["57204841219","David Llulluy-Nu\u00f1ez"],["57211666738","Beatriz Bayl\u00f3n-Gonzales"],
  ["58077315000","Meyluz Paico-Campos"],["57207915215","Laberiano Andrade-Arenas"],
  ["57016156500","Alexi Delgado"],["36659719000","Avid Roman-Gonzalez"]
];
const CONOCIDOS={"57205596738":[74,319],"36659719000":[220,913]};
let pendingRows=[];
let td=0,tc=0,cc=0,cd=0,er=0;

async function retryAuthor(idx){
  const st=document.getElementById("status");
  const[id,nom]=IDS[idx];
  st.textContent="Reintentando "+nom+"...";
  try{
    await new Promise(r=>setTimeout(r,3000));
    const r=await fetch("/api/scopus/documents?au_id="+id);
    if(!r.ok)throw new Error("HTTP "+r.status);
    const data=await r.json();
    const docs=data?.documentos?.[id]||[];
    const n=docs.length;let s=0,m=null;
    for(const d of docs){const c=parseInt(d["citedby-count"])||0;s+=c;if(m===null)m=c;}
    const ms=m!==null?"citedby-count: "+m:"sin campo";
    const k=CONOCIDOS[id];let es="";if(k)es=" (esp: "+k[0]+"/"+k[1]+")";
    let cls="ok",txt="OK";
    if(s===0&&n>0){cls="zero";txt="CITAS 0";}
    if(n===0){cls="err";txt="SIN DOCS";}
    pendingRows[idx]={id, nom, n:n+es, s:s+es, ms, cls, txt};
    renderTable();
    st.textContent="Reintento completado para "+nom+": "+n+" docs, "+s+" citas.";
  }catch(e){
    pendingRows[idx]={id, nom, n:e.message, s:"", ms:"", cls:"err", txt:e.message};
    renderTable();
    st.textContent="Error en reintento: "+e.message;
  }
}

async function run(){
  const btn=document.getElementById("btnRun"),st=document.getElementById("status"),out=document.getElementById("output");
  btn.disabled=true;out.innerHTML="";st.textContent="Iniciando...";
  pendingRows=[];
  const rows=[];
  td=0;tc=0;cc=0;cd=0;er=0;
  for(let i=0;i<IDS.length;i++){
    const[id,nom]=IDS[i];
    st.textContent=`${i+1}/${IDS.length}: ${id}...`;
    rows[i]={id:id, nom:nom, n:"...", s:"...", ms:"...", cls:"", txt:"..."};
    pendingRows=rows.slice();renderTable();
    await new Promise(r=>setTimeout(r,3000));
    try{
      const r=await fetch("/api/scopus/documents?au_id="+id);
      if(!r.ok)throw new Error("HTTP "+r.status);
      const data=await r.json();
      let docs=data?.documentos?.[id]||[];
      if(docs.length===0 && i>0){
        await new Promise(r=>setTimeout(r,5000));
        const r2=await fetch("/api/scopus/documents?au_id="+id);
        if(r2.ok){
          const data2=await r2.json();
          docs=data2?.documentos?.[id]||[];
        }
      }
      const n=docs.length;let s=0,m=null;
      for(const d of docs){const c=parseInt(d["citedby-count"])||0;s+=c;if(m===null)m=c;}
      const ms=m!==null?"citedby-count: "+m:"sin campo";
      const k=CONOCIDOS[id];let es="";if(k)es=" (esp: "+k[0]+"/"+k[1]+")";
      let cls="ok",txt="OK";
      if(s===0&&n>0){cls="zero";txt="CITAS 0";}
      if(n===0){cls="err";txt="SIN DOCS";}
      if(s>0)cc++;if(n>0)cd++;td+=n;tc+=s;
      rows[i]={id:id, nom:nom, n:n+es, s:s+es, ms:ms, cls:cls, txt:txt};
    }catch(e){
      er++;
      rows[i]={id:id, nom:nom, n:e.message, s:"", ms:"", cls:"err", txt:e.message};
    }
    pendingRows=rows.slice();renderTable();
  }
  st.textContent="Completado. "+td+" docs, "+tc+" citas totales. "+cc+"/"+IDS.length+" con citas.";
  btn.disabled=false;
}
function renderTable(){
  const out=document.getElementById("output");
  let h='<table><thead><tr><th>#</th><th>Autor ID</th><th>Nombre</th><th>Docs</th><th>Citas</th><th>Muestra citedby</th><th>Estado</th><th>Acción</th></tr></thead><tbody>';
  const rows=pendingRows;
  for(let i=0;i<rows.length;i++){
    const r=rows[i];
    h+='<tr><td>'+(i+1)+'</td><td>'+r.id+'</td><td>'+r.nom+'</td><td>'+r.n+'</td><td>'+r.s+'</td><td>'+r.ms+'</td><td class="'+r.cls+'">'+r.txt+'</td>';
    h+='<td><button onclick="retryAuthor('+i+')" style="padding:2px 8px;font-size:.7rem;cursor:pointer;background:#ffc107;color:#333;border:none;border-radius:4px">Reintentar</button></td></tr>';
  }
  h+='<tr class="total-row"><td colspan="3">TOTAL</td><td>'+td+'</td><td>'+tc+'</td><td></td><td>'+cd+' con docs, '+cc+' con citas'+(er?", "+er+" errores":"")+'</td><td></td></tr></tbody></table>';
  out.innerHTML=h;
}
</script>
</body>
</html>""")

