document.getElementById("analyzeButton").addEventListener("click", () => {
  fetch("/analyze", { method: "GET" })
    .then(response => response.json())
    .then(data => {
      document.getElementById("result").innerHTML = `
        <h3>Resultado:</h3>
        <p>${data.signal}</p>
      `;
    })
    .catch(error => {
      console.error("Erro ao analisar a entrada:", error);
    });
});



