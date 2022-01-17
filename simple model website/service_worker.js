const sCacheName = "uncle-rober-baseball";
const aFilesToCache = [
  "./img/base.png",
  "./img/baseball (1).png",
  "./img/baseball.png",
  "./css/bootstrap-colorpicker.css",
  "./css/bootstrap-datepicker.css",
  "./css/bootstrap-theme.css",
  "./css/bootstrap.min.css",
  "./css/daterangepicker.css",
  "./css/elegant-icons-style.css",
  "./css/font-awesome.css",
  "./css/font-awesome.min.css",
  "./css/fullcalendar.css",
  "./css/jquery-jvectormap-1.2.2.css",
  "./css/jquery-ui-1.10.4.min.css",
  "./css/line-icons.css",
  "./css/owl.carousel.css",
  "./css/style-responsive.css",
  "./css/style.css",
  "./css/widgets.css",
  "./css/xcharts.min.css"
];

self.addEventListener("install", (pEvent) => {
  console.log("👷 Installed");
  pEvent.waitUntil(
    caches.open(sCacheName).then((pCache) => {
      console.log("Cached...");
      return pCache.addAll(aFilesToCache);
    })
  );
});

self.addEventListener("activate", () => console.log("👷 started!"));

self.addEventListener("fetch", (pEvent) => {
  pEvent.respondWith(
    caches
      .match(pEvent.request)
      .then((response) => {
        if (!response) {
          console.log("Network Data Requested: ", pEvent.request);
          return fetch(pEvent.request);
        }
        console.log("Cache requested for Data: ", pEvent.request);
        return response;
      })
      .catch((err) => console.log(err))
  );
});
