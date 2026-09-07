

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
            alert("✅ " + data.message);

            signupform.reset();

            window.location.href = "/dashboard";

            } else {

            alert("❌ " + (data.error || data.Error || "Signup failed."));

           }

          } catch (error) {

          message.classList.remove("hidden"); 
          message.textContent = "Something went wrong.";
          message.classList.add("error");
          console,log("Something goe swrrong!!!!");

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

            alert("✅ Login successful!");

           loginform.reset();

           window.location.href = "/dashboard";

        } else {

         alert("❌ " + (data.error || data.Error || "Login failed."));

        }

       } catch (error) {

       
       message.classList.remove("hidden"); 
       message.textContent = "Something went wrong.";
       message.classList.add("error");
       console.log("something goes wrong!!!!");

      }

    });

}