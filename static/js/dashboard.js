
const logout = document.querySelector(".logout-btn");
if (logout) {
    logout.addEventListener("click", async function(event) {
        event.preventDefault();
        try {

            const response = await fetch("/logout", {
                method: "POST"
            });
            const data = await response.json();
            if (response.ok) {
                window.location.href = "/login";
            } else {
                console.log(data.error||data.Error);
            }
        } catch (error) {

            console.log("Something went wrong.", error);

        }
    });
}


async function loadProfile() {

    try {

        const response = await fetch("/profile",{
            method:"GET"
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById("username").textContent =
                data.user.username;
        } else {
            console.log(data.error||data.Error);

        }
    } catch (error) {
        console.log("Something went wrong.", error);

    }
}
loadProfile();

async function loadtransactions() {
    console.log("loadtransactions is running");
    try {

        const response = await fetch("/transactions", {
            method: "GET"
        });
        const data = await response.json();
        
        if (response.ok) {
            const transactions = data.Transaction;
            let totalincome = 0;
            let totalexpense = 0;

            transactions.forEach(function(transaction) {

                if (transaction.type == "income") {
                    totalincome += Number(transaction.amount);
                }

                if (transaction.type == "expense") {
                    totalexpense += Number(transaction.amount);
                }

            });

            const totalbalance = totalincome - totalexpense;
            const savings = totalincome - totalexpense;

            const balance = document.getElementById("totalBalance");
            balance.textContent =
                `Rs. ${totalbalance.toLocaleString()}`;

            const income = document.getElementById("totalIncome");
            income.textContent =
                `Rs. ${totalincome.toLocaleString()}`;

            const expenses = document.getElementById("totalExpenses");
            expenses.textContent =
                `Rs. ${totalexpense.toLocaleString()}`;

            const saving = document.getElementById("savings");
            saving.textContent =
                `Rs. ${savings.toLocaleString()}`;

        }

        else {

            console.log(data.error || data.Error);

        }

    }

    catch(error) {

        console.log("Something went wrong.", error);

    }

}

loadtransactions();