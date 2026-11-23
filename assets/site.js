// 메뉴 열기·닫기
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.textContent = open ? '닫기' : '메뉴';
    });
  }

  // 첫 화면 전광판: 호가가 5만 원씩 올라 실제 낙찰가에서 멈춘다
  var board = document.querySelector('.board');
  if (!board) return;
  var out = board.querySelector('[data-price]');
  var end = parseInt(out.getAttribute('data-price'), 10);
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) { board.classList.add('done'); return; }
  var now = end - 40;
  out.textContent = now;
  var timer = setInterval(function () {
    now += 5;
    out.textContent = now;
    if (now >= end) {
      clearInterval(timer);
      setTimeout(function () { board.classList.add('done'); }, 350);
    }
  }, 420);
})();
