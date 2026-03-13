async function loadJson(path) {
  const res = await fetch(path, { cache: "no-store" });
  return res.json();
}

function buildToday(person, weights, meals) {
  const now = new Date();
  const dd = String(now.getDate()).padStart(2, "0");
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const yyyy = now.getFullYear();
  const today = `${dd}.${mm}.${yyyy}`;
  const personWeights = weights.filter(x => x.person === person && x.date === today);
  const personMeals = meals.filter(x => x.person === person && x.date === today);

  let lines = [`今日记录 - ${person}`, `日期: ${today}`, "", "体重"];
  if (personWeights.length) personWeights.forEach(x => lines.push(`- ${x.time} - ${x.weight}`));
  else lines.push("- 暂无记录");
  lines.push("", "饮食");
  if (personMeals.length) personMeals.forEach(x => lines.push(`- ${x.time} - ${x.meal_type} - ${x.content}`));
  else lines.push("- 暂无记录");
  return lines.join("\n");
}

function renderTable(containerId, rows, cols) {
  const container = document.getElementById(containerId);
  if (!rows.length) {
    container.innerHTML = "<p>暂无记录</p>";
    return;
  }
  const th = cols.map(c => `<th>${c.label}</th>`).join("");
  const tr = rows.map(row => `<tr>${cols.map(c => `<td>${row[c.key] ?? ""}</td>`).join("")}</tr>`).join("");
  container.innerHTML = `<table><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>`;
}

async function refresh() {
  const person = document.getElementById("personSelect").value;
  const [weights, meals] = await Promise.all([
    loadJson("../data/weights.json"),
    loadJson("../data/meals.json"),
  ]);
  document.getElementById("todayBox").textContent = buildToday(person, weights, meals);
  const filteredWeights = weights.filter(x => x.person === person).slice().reverse();
  const filteredMeals = meals.filter(x => x.person === person).slice().reverse();
  renderTable("weightsTable", filteredWeights, [
    { key: "date", label: "日期" },
    { key: "time", label: "时间" },
    { key: "weight", label: "体重" },
  ]);
  renderTable("mealsTable", filteredMeals, [
    { key: "date", label: "日期" },
    { key: "time", label: "时间" },
    { key: "meal_type", label: "餐别" },
    { key: "content", label: "内容" },
  ]);
}

document.getElementById("refreshBtn").addEventListener("click", refresh);
document.getElementById("personSelect").addEventListener("change", refresh);
refresh();
