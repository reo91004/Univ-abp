// Firebase 초기화
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js";
import { getFirestore, collection, getDocs } from "https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js";

document.addEventListener("DOMContentLoaded", async function () {
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

	// 데이터셋 목록 (T01~T17) 및 각 데이터셋에 대한 정보
	// 실제 표시할 때는 데이터셋 내 지표(컬럼) 이름에 맞게 labels를 조정해야 합니다.
	const datasets = [
		{ id: "T01_PovertyIndicators", title: "빈곤 지표 (T01)" },
		{ id: "T02_FoodIndicators", title: "식량 지표 (T02)" },
		{ id: "T03_HealthIndicators", title: "건강 지표 (T03)" },
		{ id: "T04_EducationIndicators", title: "교육 지표 (T04)" },
		{ id: "T05_GenderEqualityIndicators", title: "성평등 지표 (T05)" },
		{ id: "T06_WaterAndSanitationIndicators", title: "물과 위생 지표 (T06)" },
		{ id: "T07_EnergyIndicators", title: "에너지 지표 (T07)" },
		{ id: "T08_EconomicGrowthIndicators", title: "경제성장 지표 (T08)" },
		{ id: "T09_IndustryInnovationInfrastruc", title: "산업·혁신·인프라 지표 (T09)" },
		{ id: "T10_ReduceInequalityIndicators", title: "불평등 감소 지표 (T10)" },
		{ id: "T11_UrbanizationIndicators", title: "도시화 지표 (T11)" },
		{ id: "T12_SustainableConsumptionProdu", title: "지속가능소비·생산 지표 (T12)" },
		{ id: "T13_ClimateActionIndicators", title: "기후행동 지표 (T13)" },
		{ id: "T14_MarineEcosystemIndicators", title: "해양생태계 지표 (T14)" },
		{ id: "T15_TerrestrialEcosystemIndicat", title: "육상생태계 지표 (T15)" },
		{ id: "T16_PeaceJusticeIndicators", title: "평화·정의 지표 (T16)" },
		{ id: "T17_GlobalPartnershipIndicators", title: "글로벌 파트너십 지표 (T17)" },
	];

	// 초기 선택 데이터셋과 탭 설정 (예: T09)
	let currentDataset = "T09_IndustryInnovationInfrastruc";
	let currentTab = null; // 현재 선택된 지표 필드명

	// 사이드바에 데이터셋 리스트 출력
	const datasetListElem = document.getElementById("dataset-list");
	datasets.forEach((ds) => {
		const li = document.createElement("li");
		li.textContent = ds.title;
		li.setAttribute("data-dataset", ds.id);
		if (ds.id === currentDataset) {
			li.classList.add("active-dataset");
		}
		li.addEventListener("click", () => {
			document.querySelectorAll("#dataset-list li").forEach((el) => el.classList.remove("active-dataset"));
			li.classList.add("active-dataset");
			currentDataset = ds.id;
			loadDatasetAndBuildTabs();
		});
		datasetListElem.appendChild(li);
	});

	// Firestore에서 해당 데이터셋 불러오기
	async function loadDataFromFirestore(datasetName) {
		const querySnapshot = await getDocs(collection(db, datasetName));
		const data = [];
		querySnapshot.forEach((doc) => {
			data.push(doc.data());
		});
		return data;
	}

	// 특정 dataset의 indicators(즉, 컬럼명들) 추출
	function getIndicatorsFromData(data) {
		if (data.length === 0) return [];
		const keys = Object.keys(data[0]);
		// "년도" 같은 주요 필드는 제외하고, 나머지를 지표로 간주
		return keys.filter((k) => k !== "년도");
	}

	// 탭 생성
	function createTabs(indicators) {
		const tabsContainer = document.getElementById("tabs");
		tabsContainer.innerHTML = "";

		indicators.forEach((indicator, index) => {
			const tabBtn = document.createElement("div");
			tabBtn.classList.add("tab-button");
			tabBtn.textContent = indicator;
			tabBtn.setAttribute("data-tab", indicator);
			if (index === 0) {
				tabBtn.classList.add("active");
				currentTab = indicator;
			}
			tabBtn.addEventListener("click", () => {
				document.querySelectorAll(".tab-button").forEach((btn) => btn.classList.remove("active"));
				tabBtn.classList.add("active");
				currentTab = indicator;
				drawChart();
			});
			tabsContainer.appendChild(tabBtn);
		});
	}

	let loadedData = [];

	async function loadDatasetAndBuildTabs() {
		loadedData = await loadDataFromFirestore(currentDataset);
		const indicators = getIndicatorsFromData(loadedData);
		createTabs(indicators);
		drawChart();
	}

	// 차트 그리기
	function drawChart() {
		if (!loadedData || loadedData.length === 0 || !currentTab) return;
		const labels = loadedData.map((item) => item["년도"]);
		const dataValues = loadedData.map((item) => item[currentTab]);

		const ctx = document.getElementById("indicatorChart").getContext("2d");
		if (window.indicatorChart && typeof window.indicatorChart.destroy === "function") {
			window.indicatorChart.destroy();
		}

		window.indicatorChart = new Chart(ctx, {
			type: "line",
			data: {
				labels: labels,
				datasets: [
					{
						label: currentTab,
						data: dataValues,
						borderColor: "rgba(54, 162, 235, 1)",
						borderWidth: 2,
						fill: false,
						tension: 0.1,
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
				scales: {
					x: {
						title: {
							display: true,
							text: "년도",
						},
					},
					y: {
						title: {
							display: true,
							text: currentTab,
						},
					},
				},
			},
		});
	}

	// 초기 로딩
	await loadDatasetAndBuildTabs();

	// Naver Maps 지도 표시
	const jeollabukdo = new naver.maps.LatLng(35.7175, 127.153); // 전라북도 좌표
	const map = new naver.maps.Map("map", {
		center: jeollabukdo,
		zoom: 7,
	});

	// 마커 대신 원형으로 전라북도를 표시
	const circle = new naver.maps.Circle({
		map: map,
		center: jeollabukdo,
		radius: 50000, // 원의 반경 (미터 단위) - 필요에 따라 조정
		strokeColor: "#5347AA",
		strokeOpacity: 1,
		strokeWeight: 2,
		fillColor: "#CFE7FF",
		fillOpacity: 0.5,
	});
});
