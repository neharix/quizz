let image_field_checkbox = document.querySelector("#image_checkbox");
let filebox = document.querySelector("#filebox");

image_field_checkbox.addEventListener("change", function() {
    if (this.checked) {
        filebox.style = "display: block !important;";
    } else {
        filebox.style = "display: none !important;";
    }
})