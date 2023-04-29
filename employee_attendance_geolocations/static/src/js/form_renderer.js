/** @odoo-module **/

/* Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

import { FormRenderer } from "@web/views/form/form_renderer";
import { usePager } from "@web/search/pager_hook";
import { patch } from "@web/core/utils/patch";
import ajax from 'web.ajax';
import core from 'web.core';
const { onMounted, onWillStart } = owl;
const _t = core._t;
const options = {
    imagePath: '/employee_attendance_geolocations/static/src/lib/m',
    imageExtension: 'png'
};


patch(FormRenderer.prototype, 'employee_attendance_geolocations.google_map_wizard', {

    setup(){
        this._super.apply(this, arguments);
        var self = this;
        onMounted(() => {
            if (self.props.record.resModel == 'employee.attendance.location.wizard') {
              self._renderEmployeeLocationOnMap();
              if (self.props.record.data.active_cluster) {
                self.filter = {};
                self._renderFilter();
              }
            }
        });
    },

    _renderFilter: async function () {
        var self = this;
        this.$filter =  $(core.qweb.render('employee_attendance_geolocations.employee_attendance_geolocations_filter', {today: (new Date()).toISOString().split('T')[0]}))
        this.$map.before(this.$filter);
        this.$filter.find('input').change(function () {
          self._getSearchDomain();
          self._renderEmployeeLocationOnMap();
        })
        this.$filter.find('.search_item').keyup(function(event) {
          if (event.keyCode === 13) {
            self._getSearchDomain();
            self._renderEmployeeLocationOnMap();
          }
        });
    },

    _getSearchDomain: function () {
        var self = this;
        if (this.$filter) {
          this.filter.search_field = self.$filter.find('select').find(":selected").attr('field');
          this.$filter.find('input').each(function () {
            var val = $(this).val();
            if (val.length > 0) {
              self.filter[$(this).attr('name')] = val;
            } else {
              self.filter[$(this).attr('name')] = false;
            }
          });
        }
    },

    _renderEmployeeLocationOnMap: async function () {
        var self = this;
        this.$map = $(".o_form_sheet").find('#employee_location');
        this.markers = [];
        var response = await ajax.jsonRpc(
          '/hr_attendance_geolocation',
          'call',
          {
            hr_attendance_ids: self.props.record.data.hr_attendance_ids.context.active_ids,
            filter: self.filter
          }
        );

        this.map_data = response.emp_attendances;
        this.active_address = response.active_address;
        this.header_info = response.header_info;
        console.log(response);
        console.log(window.hasOwnProperty('google'));
        if (!window.hasOwnProperty('google')) {
          console.log(response.google_js);
          await $.getScript(response.google_js);
        }
        this.bounds = new google.maps.LatLngBounds();
        this.infoWindow = new google.maps.InfoWindow();
        this.map = new google.maps.Map(this.$map[0], {
            zoom: 2,
            center: {lat:0, lng: 0}
        });

        this._addLocationMarker();
        this.map.fitBounds(this.bounds);
        if (this.props.record.data.active_cluster) {
          if (this.$filter) {
            this.$filter.find('h2').text(this.header_info);
          }
          new MarkerClusterer(this.map, this.markers, options);
        }
        google.maps.event.addListener(this.map, 'click', function() {
          self.infoWindow.close();
        });

    },

    _addLocationMarker: function () {
        for (var _index in this.map_data) {
          var latLng = new google.maps.LatLng(this.map_data[_index].lat, this.map_data[_index].long);
          var marker = new google.maps.Marker({
              map: this.map,
              position: latLng
          });
          this.bounds.extend(marker.position);
          this.init_popover(marker, this.map_data[_index]);
          this.markers.push(marker);
        }
    },

    init_popover: async function (marker, employee) {
        var self = this;
        if (this.active_address) {
          var content = await this._getAddressFromLatLong(employee);
          employee.address = content
          self._addMarkerPopover(marker, employee);
        } else {
          employee.address = false;
          this._addMarkerPopover(marker, employee);
        }
    },

    _addMarkerPopover: function (marker, employee) {
        var self = this;
        var onMarkerClick = function() {
          var content = self.getHtmlPopContent(employee);
          if (employee.same_location) {
            content = `
              <div class="d-flex w-100">
                <div class="col-md-6">
                  ${content}
                </div>
                <div class="col-md-6">
                  ${self.getHtmlPopContent(employee.check_out_location)}
                </div>
              </div>
            `
          }

          self.infoWindow.setContent(content);
          self.infoWindow.open(self.map, this);
        };
        google.maps.event.addListener(marker, 'click', onMarkerClick);
    },

    _getAddressFromLatLong: async function (employee) {
        this.geocoder = new google.maps.Geocoder();
        try {
          var response = await this.geocoder.geocode({ location: new google.maps.LatLng(employee.lat,employee.long)})
          if (response.results[0]) {
            return response.results[0].formatted_address;
          }
        } catch (e) {}
        return _t('Google Map geocoder is not working.');
    },

    getHtmlPopContent: function (employee) {
        var content =  `<h4 class="mt-4 font-weight-bold mb-0">
                  <span class="fa text-primary mr-2 ${employee.device_type=='mobile' ? 'fa-mobile' : 'fa-laptop'}">
                  <span class="ml-2">${employee.type}</span>
                </h4>
                <p class="mt-2 mb-0"><span class="text-primary fa fa-user-circle-o" /> <span class="text-dark ml-2">${employee.name}</span></p>
                <p class="mt4 mb-0"><span class="text-primary fa fa-calendar" /> <span class="text-dark ml-2">${employee.date}</span></p>
                <p class="mt4 mb-0"><span class="text-primary fa fa-clock-o" /> <span class="text-dark ml-2">${employee.time}</span></p>`;
        if (employee.address) {
          content += `<p class="mt4 mb-0"><span class="text-primary fa fa-address-card-o" /> <span class="ml-2 text-dark">${employee.address}</span></p>`;
        }
        if (employee.redirect_url) {
          content += `<a target="new" class="text-primary mt-2 mb-0" href="//www.google.com/maps/dir/?api=1&${employee.redirect_url}">See distance</a>`;
        }
        return content;
    },

});
