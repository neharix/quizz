const st = {};
let textarea_block = document.querySelector("#id_question").parentElement;
let textarea = document.querySelector("#id_question");
let image_block = document.querySelector("#id_image").parentElement;
let image = document.querySelector("#id_image");

image_block.style = "display: none;";

st.flap = document.querySelector('#flap');
st.toggle = document.querySelector('.toggle');

st.choice1 = document.querySelector('#choice1');
st.choice2 = document.querySelector('#choice2');

st.flap.addEventListener('transitionend', () => {

    if (st.choice1.checked) {
        st.toggle.style.transform = 'rotateY(-15deg)';
        textarea.value = "";
        textarea_block.style = "display: none;";
        image_block.style = "display: block;";
        setTimeout(() => st.toggle.style.transform = '', 400);

    } else {
        st.toggle.style.transform = 'rotateY(15deg)';
        image.value = "";
        image_block.style = "display: none;";
        textarea_block.style = "display: block;";
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