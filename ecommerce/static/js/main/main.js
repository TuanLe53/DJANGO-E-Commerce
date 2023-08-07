const account_btn = document.getElementById("account");
const user_nav = document.getElementById("user-nav");

account_btn.addEventListener("click", () => {
    if (user_nav.style.display === "none") {
        user_nav.style.display = "block";
      } else {
        user_nav.style.display = "none";
      }
})

const cart_list_btn = document.getElementById("cart_btn");
const cart_list = document.getElementById("cart");
cart_list_btn.addEventListener("click", () => {
  if (cart_list.style.display === "none") {
      cart_list.style.display = "block";
    } else {
      cart_list.style.display = "none";
    }
})