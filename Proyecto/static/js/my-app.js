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
  
  dialog:{
	  title: 'Confirmar',
	  buttonOk: 'Sí',
	  buttonCancel: 'No'
  },
  smartSelect: {
    closeOnSelect: true
  },
  
  calendar: {
	 closeOnSelect: true
  }
});
  // ... other parameters
app.on('sortableSort', function (listEl, indexes) {
  console.log(indexes);
})
var mainView = app.views.create('.view-main');

var smartSelect = app.smartSelect.create({  });


var calendarDateFormat = app.calendar.create({
  inputEl: '#demo-calendar-date-format',
  dateFormat: 'dd/mm/yyyy',
  monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
  dayNames: ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Vuernes', 'Sábado', 'Domingo'],
  dayNamesShort: ['Lun', 'Mar', 'Mier', 'Juev', 'Vier', 'Sab', 'Dom'],
});


var $$ = Dom7;
// Confirm
$$('.open-confirm').on('click', function () {
  app.dialog.confirm('Si eliminas tu perfil se eliminarán todas las cuentas añadidas.', function () {
    location.href='/DeleteProfile';
  });
});

var $$ = Dom7;
// Confirm
$$('.open-confirm1').on('click', function () {
  app.dialog.confirm('Se eliminarán todas las cuentas añadidas.', function () {
    location.href='/DeleteAccounts';
  });
});


