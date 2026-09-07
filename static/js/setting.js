const changePasswordForm =
    document.getElementById("changePasswordForm");

if (changePasswordForm) {

    changePasswordForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();

            const currentPassword =
                document.getElementById(
                    "currentPassword"
                ).value;

            const newPassword =
                document.getElementById(
                    "newPassword"
                ).value;

            const confirmPassword =
                document.getElementById(
                    "confirmPassword"
                ).value;

            const message =
                document.getElementById(
                    "passwordMessage"
                );


            if (newPassword !== confirmPassword) {

                message.textContent =
                    "New passwords do not match.";

                return;
            }


            try {

                const response = await fetch(
                    "/change-password",
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            current_password:
                                currentPassword,

                            new_password:
                                newPassword
                        })
                    }
                );


                const data =
                    await response.json();


                if (!response.ok) {
                   alert(data.error || data.Error || "Password change failed.");

                    return;
                }


                alert(data.message || "Password changed successfully!");

                changePasswordForm.reset();

            }

            catch (error) {

                console.error(error);

                message.textContent =
                    "Something went wrong.";

            }

        }
    );
}
async function loadProfile() {

    try {

        const response = await fetch("/profile", {
            method: "GET"
        });

        const data = await response.json();

        if (!response.ok) {

            console.log(
                data.error || data.Error
            );

            return;
        }

        const user = data.user;


        const username =
            document.getElementById("username");

        if (username) {
            username.textContent = user.username;
        }


        const settingsUsername =
            document.getElementById("settingsUsername");

        if (settingsUsername) {
            settingsUsername.textContent = user.username;
        }


        const settingsEmail =
            document.getElementById("settingsEmail");

        if (settingsEmail) {
            settingsEmail.textContent = user.email;
        }

    }

    catch (error) {

        console.error(
            "Error loading profile:",
            error
        );

    }
}


if (
    document.getElementById("username") ||
    document.getElementById("settingsUsername") ||
    document.getElementById("settingsEmail")
) {
    loadProfile();
}