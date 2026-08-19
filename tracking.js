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
  s.src = 'https://js.comet-serve.com/script.js?uid=cbd4d9-4503599666000007-d021d6-s&domains=start.legacyfarmer.com,app.farmermetrics.com,www.legacyfarmer.com,www.farmermetrics.com';
  document.head.appendChild(s);
})();
