
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


    const period = document.getElementById("spendingPeriod").value;
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();


    let expenses = transactions.filter(function(transaction) {
        return transaction.type === "expense";
    });


    
    // Calculate spending for each category
    const expenseofeachcategory = {};

    expenses.forEach(function(transaction) {

        const catid = transaction.category_id;

        if (!expenseofeachcategory[catid]) {

            expenseofeachcategory[catid] =
                Number(transaction.amount);

        } else {

            expenseofeachcategory[catid] +=
                Number(transaction.amount);

        }

    });


    const container =
        document.getElementById("spendingOverview");

    container.innerHTML = "";


    if (Object.keys(expenseofeachcategory).length === 0) {

        container.innerHTML =
            `<p class="no-spending">
                No spending found for this period.
            </p>`;

        return;
    }


    const amounts = Object.values(expenseofeachcategory);

    const maxAmount = Math.max(...amounts);



    Object.keys(expenseofeachcategory).forEach(function(cat) {
        const categoryname =
            categoryMap[cat] || "Unknown";

        const categoryamount =
            expenseofeachcategory[cat];

        const barWidth =
            (categoryamount / maxAmount) * 100;

        const Item =
            document.createElement("div");
        Item.classList.add("spending-bar-item");


        Item.innerHTML = `
            <div class="spending-bar-header">

                <span>${categoryname}</span>

                <strong>
                    Rs.${categoryamount.toLocaleString()}
                </strong>

            </div>

            <div class="spending-bar-background">

                <div
                    class="spending-bar"
                    style="width: ${barWidth}%">
                </div>

            </div>
        `;


        container.appendChild(Item);

    });

}

catch(error) {

    console.log(
        "Something went wrong while loading spending overview.",
        error
    );

}

}
loadspendingoverview();
const spendingPeriod =
document.getElementById("spendingPeriod");

if (spendingPeriod) {
spendingPeriod.addEventListener(
    "change",
    loadspendingoverview
);
}
