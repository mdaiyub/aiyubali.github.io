// Minimal JS: mobile nav toggle (if needed)
document.addEventListener('DOMContentLoaded', function(){
  const btn = document.getElementById('menu-btn');
  const nav = document.getElementById('navlinks');
  if(btn){
    btn.addEventListener('click', ()=>{
      nav.classList.toggle('open');
    });
  }
});
