const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function addMsg(text, who="bot"){
  const div = document.createElement("div");
  div.className = `msg ${who}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(){
  const msg = userInput.value.trim();
  if(!msg) return;
  addMsg(msg, "user");
  userInput.value = "";
  addMsg("Thinking...", "bot");
  try{
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    const last = chatBox.querySelector(".msg.bot:last-child");
    last.textContent = data.reply || data.error || "Error";
  }catch(err){
    const last = chatBox.querySelector(".msg.bot:last-child");
    last.textContent = "Network error";
  }
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", (e)=>{ if(e.key==="Enter") sendMessage(); });

// Symptom checker
const checkBtn = document.getElementById("check-btn");
checkBtn?.addEventListener("click", async ()=>{
  const checked = Array.from(document.querySelectorAll(".grid input:checked")).map(i=>i.value);
  const age = parseInt(document.getElementById("age").value || "0", 10);
  const duration = parseInt(document.getElementById("duration").value || "0", 10);
  const result = document.getElementById("check-result");
  result.textContent = "Checking...";
  try{
    const res = await fetch("/api/symptom-check", {
      method: "POST",
      headers: { "Content-Type":"application/json" },
      body: JSON.stringify({ symptoms: checked, age, duration_days: duration })
    });
    const data = await res.json();
    if(data.error){ result.textContent = data.error; return; }
    const lines = [];
    lines.push(`Triage: ${data.triage.toUpperCase()}`);
    lines.push(data.explanation);
    if(data.matches?.length){
      lines.push("");
      lines.push("Possible matches:");
      data.matches.slice(0,4).forEach(m=>{
        lines.push(`• ${m.condition} (${m.score}) — ${m.tips}`);
      });
    }
    lines.push("");
    lines.push("This tool is not medical advice.");
    result.textContent = lines.join("\n");
  }catch(e){
    result.textContent = "Error checking symptoms.";
  }
});
