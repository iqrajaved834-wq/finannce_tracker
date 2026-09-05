

const signupform = document.getElementById("signupForm");

if (signupform) {

    signupform.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const message = document.getElementById("signupMessage");

        try {

            const response = await fetch("/signup", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })

            });

            const data = await response.json();

            message.classList.remove("hidden");

            if (response.ok) {

                message.textContent = data.message;
                message.classList.add("success");

                signupform.reset();

                window.location.href = "/dashboard";

            } else {

                message.textContent = data.error;
                message.classList.add("error");

            }

        } catch (error) {

            message.classList.remove("hidden");

            message.textContent = "Something went wrong.";

            message.classList.add("error");

        }

    });

}



const loginform = document.getElementById("loginForm");

if (loginform) {

    loginform.addEventListener("submit", async function (event) {

        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const message = document.getElementById("loginMessage");

        try {

            const response = await fetch("/login", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })

            });

            const data = await response.json();

            message.classList.remove("hidden");

            if (response.ok) {

                message.textContent = data.message;
                message.classList.add("success");

                loginform.reset();

                window.location.href = "/dashboard";

            } else {

                message.textContent = data.error;
                message.classList.add("error");

            }

        } catch (error) {

            message.classList.remove("hidden");

            message.textContent = "Something went wrong.";

            message.classList.add("error");

        }

    });

}