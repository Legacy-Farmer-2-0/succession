// Shared site-wide tracking — loaded once per page via <script src="./tracking.js">
// in the <head>. Keep this the single source of truth for pixel IDs / tracking
// snippets rather than pasting them into each page individually.

// ---- Meta Pixel (ID 373699973148175) — standard base code ----
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '373699973148175');
fbq('track', 'PageView');

// ---- Cometly ----
(function () {
  var s = document.createElement('script');
  s.src = 'https://js.comet-serve.com/script.js?uid=cbd4d9-4503599666000007-d021d6-s&domains=start.legacyfarmer.com,app.farmermetrics.com,www.legacyfarmer.com,www.farmermetrics.com,succession.legacyfarmer.com';
  document.head.appendChild(s);
})();
// ---- Google tag (gtag.js) -- container GT-M34VGDJG, linked destination AW-16735868721 ----
(function () {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=GT-M34VGDJG';
    document.head.appendChild(s);
})();
window.dataLayer = window.dataLayer || [];
function gtag(){ dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'GT-M34VGDJG');

// ---- HubSpot tracking (portal 43573758) ----
(function () {
    var s = document.createElement('script');
    s.type = 'text/javascript';
    s.id = 'hs-script-loader';
    s.async = true;
    s.defer = true;
    s.src = '//js.hs-scripts.com/43573758.js';
    document.head.appendChild(s);
})();

// ---- Whop ----
!function(w,d,s,u,n,a,b){if(w[n])return;a=w[n]={q:[],t:+new Date,s:[],o:u,track:function(){a.q.push([+new Date].concat([].slice.call(arguments)))},setScope:function(){a.s=[].slice.call(arguments).filter(function(x){return typeof x==="string"});a.q.push([+new Date,"setScope"].concat(a.s))},scope:function(){var c=[].slice.call(arguments);return{track:function(){a.q.push([+new Date].concat([].slice.call(arguments)).concat([{__scope:c}]))}}}};b=d.createElement(s);b.async=1;b.src=u+"/s.js";d.getElementsByTagName(s)[0].parentNode.insertBefore(b,d.getElementsByTagName(s)[0])}(window,document,"script","https://t.whop.tw","whop");
whop.setScope("biz_99v9kJksuacARW", "biz_CIZURSEEYGqZft", "biz_quHW8e0DQkrwUy");
whop.track("page");
