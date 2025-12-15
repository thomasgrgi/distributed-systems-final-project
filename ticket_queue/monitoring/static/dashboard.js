async function startLoad() {
  const rate = document.getElementById("rate").value;

  const res = await fetch("/load?rate_per_minute=" + rate, {
    method: "POST"
  });

  const data = await res.json();
  document.getElementById("loadStatus").innerText =
    "Load running: " + data.rate + " joins/min";
}

async function stopLoad() {
  await fetch("/stop_load", { method: "POST" });
  document.getElementById("loadStatus").innerText = "Load stopped";
}

async function refresh() {
  const res = await fetch("/stats");
  const data = await res.json();

  document.getElementById("requests").innerText = data.join_requests;

  const queue = document.getElementById("queue");
  queue.innerHTML = "";
  data.queue.forEach(t => {
    const li = document.createElement("li");
    li.innerText = "Ticket " + t;
    queue.appendChild(li);
  });

  const workers = document.getElementById("workers");
  workers.innerHTML = "";
  for (const [worker, ticket] of Object.entries(data.workers)) {
    const li = document.createElement("li");
    li.innerText = `${worker} → Ticket ${ticket}`;
    workers.appendChild(li);
  }
}

setInterval(refresh, 1000);
refresh();
