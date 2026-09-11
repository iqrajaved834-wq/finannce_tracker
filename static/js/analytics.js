const analyticsPeriod = document.getElementById("analyticsPeriod");

if (analyticsPeriod) {

    analyticsPeriod.addEventListener("change", function () {

        const period = analyticsPeriod.value;
        window.location.href = `/analytics?period=${period}`;

    });

}