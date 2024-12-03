// Firebase 초기화
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js";

document.addEventListener("DOMContentLoaded", function () {
	// Firebase 설정
	const firebaseConfig = {
		apiKey: "AIzaSyAEbozruGS6f9G7SRBOwmazQZjsPDODIoY",
		authDomain: "abp-sdgs.firebaseapp.com",
		projectId: "abp-sdgs",
		storageBucket: "abp-sdgs.firebasestorage.app",
		messagingSenderId: "1029076477606",
		appId: "1:1029076477606:web:29d7f8ec49733b8a2df667",
	};

	const app = initializeApp(firebaseConfig);
	const db = getFirestore(app);

	// Firestore에서 데이터 불러오기
	async function loadDataFromFirestore() {
		const querySnapshot = await getDocs(collection(db, "T9_IndustryInnovationInfrastruc"));
		const data = [];
		querySnapshot.forEach((doc) => {
			data.push(doc.data());
		});
		return data;
	}

	// Chart.js를 사용하여 차트 생성
	function createChart(data, tab) {
		const labels = data.map((item) => item["년도"]);
		const dataValues = data.map((item) => item[tab]);

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
	}

	loadDataFromFirestore().then((data) => {
		createChart(data, "A9_1_1_사계절도로접근성비율"); // 기본 탭 설정
	});

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
		loadDataFromFirestore().then((data) => {
			createChart(data, tab);
		});
	});

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
