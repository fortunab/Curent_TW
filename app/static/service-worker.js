if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('./service-worker.js')
    .then(function(registration) {
        console.log('Service Worker Registered!');
        return registration;
    })
    .catch(function(err) {
        console.error('Unable to register service worker.', err);
    });
}

const CACHE_NAME = 'static-cache';
const FILES_TO_CACHE = [
  '/static/offline.html',
    '/static/notificareaPush.html',
];

self.addEventListener('install', (evt) => {
  console.log('[ServiceWorker] Install');
  evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline page');
      return cache.addAll(FILES_TO_CACHE);
    })
  );

  self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
  console.log('[ServiceWorker] Activate');
  evt.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(event) {
  event.respondWith(fetch(event.request));
});


self.addEventListener('fetch', (evt) => {
  if (evt.request.mode !== 'navigate') {
    return;
  }
  evt.respondWith(fetch(evt.request).catch(() => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match('offline.html');
      });
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request).catch(function() {
      return caches.match(event.request);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});


const pushButton = document.getElementById('push-btn');

if (!("Notification" in window)) {
    pushButton.hidden;
  }
pushButton.addEventListener('click', askPermission);

function askPermission(evt) {
  pushButton.disabled = true;
  Notification.requestPermission().then(function(permission) {
    notificationButtonUpdate();
   });
}

function notificationButtonUpdate() {
  if (Notification.permission == 'granted') {
    pushButton.disabled = true;
  } else {
    pushButton.disabled = false;
  }
}

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');

  const title = 'Notificari';
  const options = {
    body: event.data.text(),
    icon: 'static/assets/img/1.jpg',
    vibrate: [50, 50, 50],
    sound: 'static/audio/notification-sound.mp3'
  };
  event.waitUntil(self.registration.showNotification(title, options));
});


var swRegistration = null;
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('./service-worker.js')
    .then(function(registration) {
        console.log('Service Worker Registered!');
        swRegistration = registration;
        return registration;
    })
    .catch(function(err) {
        console.error('Unable to register service worker.', err);
    });
}

self.addEventListener('sync', function(event) {
  if (event.tag == 'example-tag') {
    event.waitUntil(
    // Actions to be performed go here.
    );
  }
});

navigator.serviceWorker.ready.then(function(swRegistration) {
  return swRegistration.sync.register('example-tag');
});

