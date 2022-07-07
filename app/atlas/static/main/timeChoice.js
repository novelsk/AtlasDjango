jQuery.datetimepicker.setLocale('en');
const timeFields = Array.from(document.getElementsByClassName("choices"));
let timeChoices = [];
for (const key in timeFields) {
    timeChoices.push(jQuery(timeFields[key]).datetimepicker({format:'d.m.Y H:i:s'}));
}
