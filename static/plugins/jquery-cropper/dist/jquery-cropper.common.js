/*!
 * jQuery Cropper v1.0.0
 * https://github.com/fengyuanchen/jquery-cropper
 *
 * Copyright (c) 2020 Chen Fengyuan
 * Released under the MIT license
 *
 * Date: 2020-04-01T06:20:13.168Z
 */

'use strict';

function _interopDefault (ex) { return (ex && (typeof ex === 'object') && 'default' in ex) ? ex['default'] : ex; }

var $ = _interopDefault(require('jquery'));
var Cropper = _interopDefault(require('cropperjs'));

if ($.fn) {
  var AnotherCropper = $.fn.cropper;
  var NAMESPACE = 'cropper';

  $.fn.cropper = function jQueryCropper(option) {
    for (var _len = arguments.length, args = Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
      args[_key - 1] = arguments[_key];
    }

    var result = void 0;

    this.each(function (i, element) {
      var $element = $(element);
      var isDestroy = option === 'destroy';
      var cropper = $element.data(NAMESPACE);

      if (!cropper) {
        if (isDestroy) {
          return;
        }

        var options = $.extend({}, $element.data(), $.isPlainObject(option) && option);

        cropper = new Cropper(element, options);
        $element.data(NAMESPACE, cropper);
      }

      if (typeof option === 'string') {
        var fn = cropper[option];

        if ($.isFunction(fn)) {
          result = fn.apply(cropper, args);

          if (result === cropper) {
            result = undefined;
          }

          if (isDestroy) {
            $element.removeData(NAMESPACE);
          }
        }
      }
    });

    return result !== undefined ? result : this;
  };

  $.fn.cropper.Constructor = Cropper;
  $.fn.cropper.setDefaults = Cropper.setDefaults;
  $.fn.cropper.noConflict = function noConflict() {
    $.fn.cropper = AnotherCropper;
    return this;
  };
}
