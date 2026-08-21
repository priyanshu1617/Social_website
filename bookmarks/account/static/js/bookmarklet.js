(function(){
  if (window.myBookmarklet !== undefined) {
    myBookmarklet();
  } else {
    document.body.appendChild(document.createElement('script')).src='https://mysite.com/static/js/bookmarklet.js';
  }
})();
