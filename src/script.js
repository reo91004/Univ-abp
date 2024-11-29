document.addEventListener("DOMContentLoaded", function () {
	// 네비게이션 바
	$("#navbar a").on("click", function (event) {
		// event.preventDefault();
		// alert("This link is currently not functional.");
	});

	// 탭 클릭 이벤트 처리
	$(".tab-button").on("click", function () {
		$(".tab-button").removeClass("active");
		$(this).addClass("active");
		const tab = $(this).data("tab");
		loadData(tab);
	});

	// 기본 탭 설정
	loadData("A9_1_1_사계절도로접근성비율");

	function loadData(tab) {
		$.ajax({
			url: `http://127.0.0.1:5001/data?table=${tab}`,
			method: "GET",
			success: function (response) {
				const labels = response.map((item) => item["년도"]);
				const dataValues = response.map((item) => item[tab]);
				console.log(response);

				// Chart.js 그래프 생성
				const ctx = document.getElementById("energyChart").getContext("2d");
				if (window.energyChart && typeof window.energyChart.destroy === "function") {
					window.energyChart.destroy();
				}
				window.energyChart = new Chart(ctx, {
					type: "line",
					data: {
						labels: labels,
						datasets: [
							{
								label: tab,
								data: dataValues,
								borderColor: "rgba(255, 99, 132, 1)",
								borderWidth: 2,
								fill: false,
							},
						],
					},
					options: {
						responsive: true,
						plugins: {
							legend: {
								display: true,
								position: "top",
							},
						},
					},
				});
			},
			error: function (error) {
				console.error("데이터를 불러오는 중 오류가 발생했습니다:", error);
			},
		});
	}

	// Naver Maps 지도 표시
	const jeollabukdo = new naver.maps.LatLng(35.7175, 127.153); // 전라북도 좌표
	const map = new naver.maps.Map("map", {
		center: jeollabukdo,
		zoom: 7,
	});

	// 마커 추가 (전라북도 위치)
	const marker = new naver.maps.Marker({
		position: jeollabukdo,
		map: map,
		title: "전라북도",
	});
});
