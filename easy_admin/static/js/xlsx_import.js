const st = {};
let image_field_checkbox = document.querySelector("#image_checkbox");
let flap_toggle = document.querySelector("#toggle-wrap");
let filebox = document.querySelector("#filebox");

st.flap = document.querySelector('#flap');
st.toggle = document.querySelector('.toggle');

st.choice1 = document.querySelector('#choice1');
st.choice2 = document.querySelector('#choice2');

image_field_checkbox.addEventListener("change", function() {
    if (this.checked) {
        flap_toggle.style = "display: flex !important;";
        filebox.style = "display: block !important;";
    } else {
        flap_toggle.style = "display: none !important;";
        filebox.style = "display: none !important;";
    }
})

st.flap.addEventListener('transitionend', () => {
    if (st.choice1.checked) {
        st.toggle.style.transform = 'rotateY(-15deg)';
        filebox.innerHTML = "";
        for (let i = 1; i <= 10; i++) {
            let image_label = document.createElement("label");
            let image_input = document.createElement("input");
            image_label.setAttribute("for", "image" + String(i));
            image_label.classList.add("my-2");
            image_label.innerHTML = "Surat " + String(i) + ":";
            image_input.type = "file";
            image_input.classList.add("form-control");
            image_input.classList.add("my-2");
            image_input.id = "image" + String(i);
            image_input.name = "image" + String(i);
            filebox.appendChild(image_label);
            filebox.appendChild(image_input);
        }
        setTimeout(() => st.toggle.style.transform = '', 400);
    } else {
        st.toggle.style.transform = 'rotateY(15deg)';
        filebox.innerHTML = "";
        let zip_label = document.createElement("label");
        let zip_input = document.createElement("input");
        zip_label.setAttribute("for", "zipfile");
        zip_label.classList.add("my-2");
        zip_label.innerHTML = "ZIP faýl:";
        zip_input.type = "file";
        zip_input.classList.add("form-control");
        zip_input.classList.add("my-2");
        zip_input.id = "zipfile";
        zip_input.name = "zipfile";
        filebox.appendChild(zip_label);
        filebox.appendChild(zip_input);
        setTimeout(() => st.toggle.style.transform = '', 400);
    }

})

st.clickHandler = (e) => {

    if (e.target.tagName === 'LABEL') {
        setTimeout(() => {
            st.flap.children[0].textContent = e.target.textContent;
        }, 250);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    st.flap.children[0].textContent = st.choice2.nextElementSibling.textContent;
});

document.addEventListener('click', (e) => st.clickHandler(e));