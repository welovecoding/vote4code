function initPostView() {
  $('pre code').each(function (i, block) {
    hljs.highlightBlock(block);
    hljs.lineNumbersBlock(block);
  });
}
