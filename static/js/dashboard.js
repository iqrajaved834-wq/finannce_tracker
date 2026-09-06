
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

async function loadrecenttransactions(){
    try{
        const response=await fetch("/transactions",{
            method:"GET"
        });
        const data=await response.json();
        if(!response.ok){
            console.log([data.error]||[data.Error])
        }
        const transactions =data.Transaction;


        const response2=await fetch("/categories",{
            method:"GET"
        });
        const data2= await response2.json();
        if(!response.ok){
            console.log([data.error]||[data.Error])
        }
        const categories=data2.Categories;
        

       
        const categoryMap = {};
        categories.forEach(function(category) {
        categoryMap[category.category_id] = category.name;
        });
        const rescenttransactions=transactions.slice(0,5);
        

        const container=document.getElementById("recentTransactions");
        container.innerHTML="";

        if(rescenttransactions.length===0){
            container.innerHTML=
            "<p> NO TRANSACTION YET! </p>";
             return;
             }


        rescenttransactions.forEach(function(tran){
            const categoryname=categoryMap[tran.category_id]||"";
            const amountClass=tran.type==="income"?"transaction_income":"transaction_expense";
            const amountsign=tran.type==="income"?"+":"-";


            const transactionItem=document.createElement("div");
            transactionItem.classList.add("transaction_item");

       
            transactionItem.innerHTML=
            `<div class="transaction_information">
             <strong> ${categoryname}</strong>
             <span> ${tran.description}</span>
             </div>
             <div class="transaction_amount">
             <strong class="${amountClass}"> ${amountsign} Rs ${Number(tran.amount). toLocaleString()}</strong>
             <span><span>${tran.transaction_date}</span></span>
             </div>
            `
        container.appendChild( transactionItem);
        })

    }
    catch(error){
     console.log(
            "Something went wrong while loading recent transactions.",
            error
        );
    }
}  
loadrecenttransactions();


async function loadspendingoverview() {

    try {

        const response = await fetch("/transactions", {
            method: "GET"
        });
        const data = await response.json();
        if (!response.ok) {
            console.log(data.error || data.Error);
            return;
        }
        const transactions = data.Transaction;

        const response2 = await fetch("/categories", {
            method: "GET"
        });
        const data2 = await response2.json();
        if (!response2.ok) {
            console.log(data2.error || data2.Error);
            return;
        }
        const categories = data2.Categories;


        const categoryMap = {};
        categories.forEach(function(category) {
            categoryMap[category.category_id] = category.name;

        });

        const filteredtransactions = transactions.filter(function(transaction) {
            return transaction.type === "expense";

        });


        const period =
            document.getElementById("spendingPeriod").value;
        const today = new Date();
        const currentmonth = today.getMonth();
        const currentyear = today.getFullYear();


        const periodtransactions = filteredtransactions.filter(function(transaction) {

            const date = new Date(transaction.transaction_date);
            if (isNaN(date.getTime())) {
                return false;
            }


            const datemonth = date.getMonth();
            const dateyear = date.getFullYear();

            if (period === "this_month") {

                return (
                    datemonth === currentmonth &&
                    dateyear === currentyear
                );

            }
            if (period === "last_month") {

                let lastmonth = currentmonth - 1;
                let lastyear = currentyear;


                if (lastmonth < 0) {

                    lastmonth = 11;
                    lastyear = currentyear - 1;

                }


                return (
                    datemonth === lastmonth &&
                    dateyear === lastyear
                );

            }

            if (period === "this_year") {

                return dateyear === currentyear;

            }


            return false;

        });


        const amountofcategory = {};
        periodtransactions.forEach(function(transaction) {

            const catid = transaction.category_id;
            const amount = Number(transaction.amount);

            if (amountofcategory[catid]) {

                amountofcategory[catid] += amount;

            }
            else {

                amountofcategory[catid] = amount;

            }

        });
        const container =
            document.getElementById("spendingOverview");

        container.innerHTML = "";
        if (Object.keys(amountofcategory).length === 0) {

            container.innerHTML =
                "<p>No spending found.</p>";

            return;

        }
        const amounts =
            Object.values(amountofcategory);

        const maxamount =
            Math.max(...amounts)

        Object.keys(amountofcategory).forEach(function(cat) {

            const categoryName =
                categoryMap[cat];

            const categoryAmount =
                amountofcategory[cat];

            const percentage =
                (categoryAmount / maxamount) * 100;


            const item =
                document.createElement("div");

            item.classList.add("spending-bar-item");


            item.innerHTML = `

                <div class="spending-bar-header">

                    <span>
                        ${categoryName || "Unknown Category"}
                    </span>

                    <strong>
                        Rs.${categoryAmount.toLocaleString()}
                    </strong>

                </div>


                <div class="spending-bar-background">

                    <div
                        class="spending-bar"
                        style="width: ${percentage}%">
                    </div>

                </div>

            `;


            container.appendChild(item);

        });

    }


    catch(error) {

        console.log(
            "Something went wrong!!!!!!",
            error
        );

    }

}

const overview =
    document.getElementById("spendingPeriod");


if (overview) {

    overview.addEventListener("change", function() {

        loadspendingoverview();

    });

}


loadspendingoverview();