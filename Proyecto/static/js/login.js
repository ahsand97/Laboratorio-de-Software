var app = new Framework7({
  // App root element
  root: '#app',
  // App Name
  name: 'My App',
  // App id
  id: 'com.myapp.test',
  // Enable swipe panel
  panel: {
    swipe: 'left',
  },
  // Add default routes
  routes: [
    {
      path: '/login/',
      url: '../login.html',
    },
  ],
  // ... other parameters
});

var mainView = app.views.create('.view-main');

var $$ = Dom7;

$$('#my-login-screen .login-screen').on('pageInit', function () {
  // Close login screen
  app.loginScreen.open('#my-login-screen');
});



