const st = {};
let textarea_block = document.querySelector("#id_answer").parentElement;
let textarea = document.querySelector("#id_answer");
let image_block = document.querySelector("#id_image").parentElement;
let image = document.querySelector("#id_image");
let is_true_checkbox = document.querySelector("#id_is_true");



is_true_checkbox.parentElement.setAttribute("class", "form-check form-switch");
is_true_checkbox.parentElement.innerHTML = "Dogry jogapmy?" + is_true_checkbox.parentElement.innerHTML;



image_block.style = "display: none;";

st.flap = document.querySelector('#flap');
st.toggle = document.querySelector('.toggle');

st.choice1 = document.querySelector('#choice1');
st.choice2 = document.querySelector('#choice2');

st.flap.addEventListener('transitionend', () => {

    if (st.choice1.checked) {
        st.toggle.style.transform = 'rotateY(-15deg)';
        textarea.innerHTML = "";
        textarea.value = "";
        textarea.removeAttribute("required");
        image.setAttribute("required", "");
        textarea_block.style = "display: none;";
        image_block.style = "display: block;";
        setTimeout(() => st.toggle.style.transform = '', 400);
    } else {
        st.toggle.style.transform = 'rotateY(15deg)';
        image.value = "";
        image_block.style = "display: none;";
        image.removeAttribute("required");
        textarea.setAttribute("required", "");
        textarea_block.style = "display: block;";
        textarea.innerHTML = "";
        textarea.value = "";
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