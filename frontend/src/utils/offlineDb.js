// Offline IndexedDB and LocalStorage abstraction for synchronization

const DB_NAME = 'farmapp_offline_db';
const DB_VERSION = 1;
const QUEUE_STORE = 'sync_queue';
const CACHE_STORE = 'master_cache';

const openDb = () => {
  return new Promise((resolve, reject) => {
    if (!window.indexedDB) {
      resolve(null);
      return;
    }
    const request = window.indexedDB.open(DB_NAME, DB_VERSION);
    request.onerror = () => resolve(null);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains(QUEUE_STORE)) {
        db.createObjectStore(QUEUE_STORE, { keyPath: 'id', autoIncrement: true });
      }
      if (!db.objectStoreNames.contains(CACHE_STORE)) {
        db.createObjectStore(CACHE_STORE, { keyPath: 'key' });
      }
    };
  });
};

export const offlineDb = {
  getPendingQueue: async () => {
    try {
      const db = await openDb();
      if (!db) {
        const saved = localStorage.getItem('farmapp_sync_queue');
        return saved ? JSON.parse(saved) : [];
      }
      return new Promise((resolve) => {
        const tx = db.transaction(QUEUE_STORE, 'readonly');
        const store = tx.objectStore(QUEUE_STORE);
        const req = store.getAll();
        req.onsuccess = () => resolve(req.result || []);
        req.onerror = () => resolve([]);
      });
    } catch (e) {
      return [];
    }
  },

  enqueueOperation: async (operation) => {
    try {
      const opWithMeta = {
        ...operation,
        timestamp: new Date().toISOString(),
      };
      const db = await openDb();
      if (!db) {
        const saved = localStorage.getItem('farmapp_sync_queue');
        const queue = saved ? JSON.parse(saved) : [];
        queue.push({ ...opWithMeta, id: Date.now() });
        localStorage.setItem('farmapp_sync_queue', JSON.stringify(queue));
        return;
      }
      return new Promise((resolve) => {
        const tx = db.transaction(QUEUE_STORE, 'readwrite');
        const store = tx.objectStore(QUEUE_STORE);
        const req = store.add(opWithMeta);
        req.onsuccess = () => resolve(req.result);
        req.onerror = () => resolve(null);
      });
    } catch (e) {
      console.error('Failed to enqueue offline operation', e);
    }
  },

  clearQueue: async () => {
    try {
      const db = await openDb();
      if (!db) {
        localStorage.removeItem('farmapp_sync_queue');
        return;
      }
      return new Promise((resolve) => {
        const tx = db.transaction(QUEUE_STORE, 'readwrite');
        const store = tx.objectStore(QUEUE_STORE);
        const req = store.clear();
        req.onsuccess = () => resolve(true);
        req.onerror = () => resolve(false);
      });
    } catch (e) {
      console.error('Failed to clear queue', e);
    }
  },

  cacheMasterData: async (data) => {
    try {
      const db = await openDb();
      if (!db) {
        localStorage.setItem('farmapp_master_cache', JSON.stringify(data));
        return;
      }
      return new Promise((resolve) => {
        const tx = db.transaction(CACHE_STORE, 'readwrite');
        const store = tx.objectStore(CACHE_STORE);
        const req = store.put({ key: 'master_data', data, timestamp: Date.now() });
        req.onsuccess = () => resolve(true);
        req.onerror = () => resolve(false);
      });
    } catch (e) {
      console.error('Failed to cache master data', e);
    }
  },
};
