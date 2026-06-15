/* ============================================================
   deck.js — GSAP mission manual engine
   GSAP enhanced · readable fallback · reduced-motion safe
   ============================================================ */
(function(){
  "use strict";
  var doc=document;
  var root=doc.documentElement;
  var reduce=window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var gsapOK=!!(window.gsap);
  var stOK=!!(window.gsap && window.ScrollTrigger);
  var progress=doc.querySelector('.progress');
  var railFill=doc.querySelector('.chapter-progress span');

  function updateProgress(){
    var h=doc.documentElement;
    var max=h.scrollHeight-h.clientHeight;
    var p=max>0?(h.scrollTop||doc.body.scrollTop)/max:0;
    if(progress) progress.style.width=(p*100).toFixed(2)+'%';
    if(railFill) railFill.style.height=(p*100).toFixed(2)+'%';
  }
  window.addEventListener('scroll', updateProgress, {passive:true});
  window.addEventListener('resize', updateProgress, {passive:true});
  updateProgress();

  function fillBars(){
    [].slice.call(doc.querySelectorAll('.bf[data-w]')).forEach(function(bar){
      bar.style.width = bar.getAttribute('data-w') + '%';
    });
  }

  function countUp(el){
    var target = parseFloat(el.getAttribute('data-count'));
    if (Number.isNaN(target)) return;
    var suffix = el.getAttribute('data-suffix') || '';
    var prefix = el.getAttribute('data-prefix') || '';
    var decimals = target % 1 !== 0 ? 1 : 0;
    if (reduce || !window.requestAnimationFrame) {
      el.textContent = prefix + target.toFixed(decimals) + suffix;
      return;
    }
    var start = null;
    var duration = 1200;
    function tick(ts){
      if (!start) start = ts;
      var t = Math.min(1, (ts - start) / duration);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = prefix + (target * eased).toFixed(decimals) + suffix;
      if (t < 1) requestAnimationFrame(tick);
      else el.textContent = prefix + target.toFixed(decimals) + suffix;
    }
    requestAnimationFrame(tick);
  }

  function prepareRevealTargets(){
    var selectors='section, .guide-article h1, .guide-article h2, .guide-article h3, .card, .panel, .table-wrap, .code-card, .code, .callout, details, .step, .stepc, .tool, .flowcard, .note, .node, .stat';
    [].slice.call(doc.querySelectorAll(selectors)).forEach(function(el){
      if(!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal','');
    });
  }
  prepareRevealTargets();
  var revealEls=[].slice.call(doc.querySelectorAll('[data-reveal]'));

  if(gsapOK && !reduce){
    root.classList.add('js-motion');
    if(stOK) gsap.registerPlugin(ScrollTrigger);
    gsap.defaults({duration:.85,ease:'power3.out',overwrite:'auto'});

    var heroTl=gsap.timeline({defaults:{duration:.9,ease:'power3.out'}});
    heroTl.from('.hero-media',{scale:1.06,autoAlpha:.72,duration:1.4})
      .from('.mission-kicker',{y:18,autoAlpha:0},'<.12')
      .from('.mission-hero h1 .line',{y:52,autoAlpha:0,stagger:.09},'<.08')
      .from('.hero-lead',{y:24,autoAlpha:0},'<.2')
      .from('.btn',{y:16,autoAlpha:0},'<.12')
      .from('.hero-telemetry span',{y:18,autoAlpha:0,stagger:.06},'<.1');

    if(stOK){
      gsap.to('.hero-media',{yPercent:7,ease:'none',scrollTrigger:{trigger:'.mission-hero',start:'top top',end:'bottom top',scrub:1}});
      ScrollTrigger.batch(revealEls,{start:'top 86%',once:true,interval:.08,batchMax:6,onEnter:function(batch){gsap.to(batch,{autoAlpha:1,y:0,stagger:.07,clearProps:'visibility'});batch.forEach(function(el){el.classList.add('is-visible');});}});
      ScrollTrigger.batch('[data-count]',{start:'top 84%',once:true,onEnter:function(batch){batch.forEach(countUp);}});
      ScrollTrigger.create({trigger:doc.querySelector('[data-bars]') || doc.getElementById('costBars') || doc.body,start:'top 84%',once:true,onEnter:fillBars});
    }else{
      gsap.to(revealEls,{autoAlpha:1,y:0,stagger:.04,onComplete:function(){revealEls.forEach(function(el){el.classList.add('is-visible');});}});
      [].slice.call(doc.querySelectorAll('[data-count]')).forEach(countUp);
      fillBars();
    }
    setTimeout(function(){revealEls.forEach(function(el){el.classList.add('is-visible');});},2600);
  }else{
    revealEls.forEach(function(el){el.classList.add('is-visible');});
    [].slice.call(doc.querySelectorAll('[data-count]')).forEach(countUp);
    fillBars();
  }

  [].slice.call(doc.querySelectorAll('.copy-button,.cp')).forEach(function(btn){
    btn.addEventListener('click',function(){
      var sel=btn.getAttribute('data-copy');
      var src=sel?doc.querySelector(sel):null;
      if(!src){var card=btn.closest('.code-card,.code,figure')||btn.parentElement;src=card?card.querySelector('pre, code'):null;}
      var text=src?(src.innerText||src.textContent):'';
      function done(){var label=btn.getAttribute('data-label')||btn.textContent||'Copy';btn.setAttribute('data-label',label);btn.classList.add('copied','done');btn.textContent='已複製';setTimeout(function(){btn.classList.remove('copied','done');btn.textContent=label;},1600);}
      if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done,done);
      else{var ta=doc.createElement('textarea');ta.value=text;doc.body.appendChild(ta);ta.select();try{doc.execCommand('copy');}catch(e){}doc.body.removeChild(ta);done();}
    });
  });

  function setDetailsOpen(open){[].slice.call(doc.querySelectorAll('details.q,details.faq,details')).forEach(function(d){if(open){if(!d.hasAttribute('data-wasopen'))d.setAttribute('data-wasopen',d.open?'1':'0');d.open=true;}else{d.open=d.getAttribute('data-wasopen')==='1';d.removeAttribute('data-wasopen');}});}
  function finalizeForPrint(){revealEls.forEach(function(el){el.classList.add('is-visible');});setDetailsOpen(true);}
  window.addEventListener('beforeprint',finalizeForPrint);
  window.addEventListener('afterprint',function(){setDetailsOpen(false);});
})();
