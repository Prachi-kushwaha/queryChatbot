
document.getElementById("askBtn")!.addEventListener("click", async () => {
  const question = (document.getElementById("question") as HTMLInputElement)!.value;

  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  chrome.tabs.sendMessage(
    tab.id!,
    { type: "GET_PAGE_CONTENT" },
    async (response:any) => {
      const pageText = response.content;

      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question,
          page_text: pageText
        })
      });

      const data = await res.json();
      document.getElementById("answer")!.innerText = data.answer;
    }
  );
});
