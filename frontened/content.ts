

function extractPageContent(){
    const removeTags = ["nav", "footer", "aside", "script", "style"]
    removeTags.forEach(tag =>{
        document.querySelectorAll(tag).forEach(el => el.remove());
    })

    const article = document.querySelector("article") ||
                    document.querySelector("main") || document.body;

                return article.innerText;

}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_PAGE_CONTENT") {
    sendResponse({ content: extractPageContent() });
  }
});