/* The API communication module.
   Inspired by Svelte RealWorld:
     https://github.com/sveltejs/realworld/blob/master/src/node_modules/api.js */

import { API_HOST } from '@/constants/env.js';
if (API_HOST == null) {
  throw new Error('The API host is undefined.');
}

function request(method, url, options) {
  const formDataClass = process.browser ? FormData : require('url').URLSearchParams;

  let actualOptions = {
    credentials: 'include',
    method,
    headers: options && options.headers || {},
  };

  if (options && 'cookie' in options) {
    actualOptions.headers['Cookie'] = options.cookie;
  }

  if (options && options.data instanceof formDataClass) {
    actualOptions.body = options.data;
  } else if (options && options.data != null) {
    actualOptions.headers['Content-Type'] = 'application/json';
    actualOptions.body = JSON.stringify(options.data);
  }

  if (this == null || this.fetch == null) {
    return window.fetch(url, actualOptions);
  }

  return this.fetch(url, actualOptions);
}

export function get(path, options) {
  return request.call(this, 'GET', API_HOST + path, options);
}

export function post(path, options) {
  return request.call(this, 'POST', API_HOST + path, options);
}

export function patch(path, options) {
  return request.call(this, 'PATCH', API_HOST + path, options);
}

export function del(path, options) {
  return request.call(this, 'DELETE', API_HOST + path, options);
}
