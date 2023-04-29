/* Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */

odoo.define('employee_attendance_geolocations.my_attendances', function (require) {
  "use strict";

  var MyAttendances = require('hr_attendance.my_attendances');
  require('web.AbstractAction');

  MyAttendances.include({

    willStart: function () {
      var self = this;
      var def = this._rpc({
          model: 'ir.config_parameter',
          method: 'get_param',
          args: ['employee_attendance_geolocations.is_required_location'],
      }).then(function (res) {
          self.is_required_location = (res == 'True');
      });
      var proms = [def, this._super.apply(this, arguments)];
      return Promise.all(proms);
    },

    do_action: function (action) {
      if (action.xml_id == 'hr_attendance.hr_attendance_action_greeting_message') {
        this._set_employee_current_position(action);
      }
      this._super.apply(this, arguments);
    },

    update_attendance: function () {
      this.position = false;
      this._emp_geolocation(this._super);
    },

    _emp_geolocation: function (__main__) {
      var self = this;
      if (navigator.geolocation) {
        var options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        };
        var success = function (position) {
          self.position = position;
          return __main__.apply(self, arguments);
        };
        var error = function (error) {
          if (!self.is_required_location) {
            return __main__.apply(self, arguments);
          } else {
            self.displayNotification({
              title: _("Please reload your browser, then active your navigator to complete check in/out process"),
              type: 'danger'
            });
          }
        };
        navigator.geolocation.getCurrentPosition(success, error, options);
      } else {
        return __main__.apply(self, arguments);
      }
    },

    _set_employee_current_position: function (action) {
      var self = this;
      if (self.position) {
        var args = [
            [action.attendance.id],
            parseFloat(self.position.coords.latitude),
            parseFloat(self.position.coords.longitude),
          ];

        if (navigator.userAgent.includes('Mobi')) {
          args.push('mobile');
        }
        self._rpc({
            model: 'hr.attendance',
            method: 'set_employee_check_in_out_location',
            args: args,
        }).then(function () {})
      }
    }

  });

})
