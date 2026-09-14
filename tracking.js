// Shared site-wide tracking — loaded once per page via <script src="./tracking.js">
// in the <head>. Keep this the single source of truth for pixel IDs / tracking
// snippets rather than pasting them into each page individually.

// ---- Meta Pixel (ID 373699973148175) — standard base code ----
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '373699973148175');
fbq('track', 'PageView');

// ---- Google Tag Manager (GTM-PKPSV9NX) — same container loaded on start.legacyfarmer.com ----
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
                    })(window,document,'script','dataLayer','GTM-PKPSV9NX');

// ---- Google tag (gtag.js) — GA4 + Google Ads, same IDs loaded on start.legacyfarmer.com ----
(function(){
  var gs = document.createElement('script');
  gs.async = true;
  gs.src = 'https://www.googletagmanager.com/gtag/js?id=G-JDK5R4HV70';
  document.head.appendChild(gs);
})();
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-JDK5R4HV70');
gtag('config', 'G-4N7281HK5V');
gtag('config', 'AW-16735868721');

// ---- Cometly ----
(function () {
  var s = document.createElement('script');
  s.src = 'https://js.comet-serve.com/script.js?uid=cbd4d9-4503599666000007-d021d6-s&domains=start.legacyfarmer.com,app.farmermetrics.com,www.legacyfarmer.com,www.farmermetrics.com,succession.legacyfarmer.com';
  document.head.appendChild(s);
})();
