//DOM
var $ = document.querySelector.bind(document);

//APP
var App = {};
App.init = function () {
	//Init
	function handleFileSelect(evt) {
		var files = evt.target.files; // FileList object

		//files template
		var template = "" + Object.keys(files).map(function (file) {
			var file_name = files[file].name;
			var name_section_width = (file_name.length * 6.2) + 30;
			if (name_section_width > 155) {
				name_section_width = 155;
			}
			var progress_width = 300 - 45 - name_section_width;

			var container_div = "<div class=\"file file--" + file + "\">\n";

			var file_name_display = "<span>" + file_name + "</span>\n";

			var name_section = "<div class=\"name\" style=\"width: ";
			name_section += name_section_width + "px;\">";
			name_section += file_name_display  + "</div>\n";

			var progress_bar = "<div class=\"progress active\" style=\"width:" + progress_width + "px;\"></div>\n";
			var success_icon = "<div class=\"done\">\n\t<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\" x=\"0px\" y=\"0px\" viewBox=\"0 0 1000 1000\">\n\t\t<g><path id=\"path\" d=\"M500,10C229.4,10,10,229.4,10,500c0,270.6,219.4,490,490,490c270.6,0,490-219.4,490-490C990,229.4,770.6,10,500,10z M500,967.7C241.7,967.7,32.3,758.3,32.3,500C32.3,241.7,241.7,32.3,500,32.3c258.3,0,467.7,209.4,467.7,467.7C967.7,758.3,758.3,967.7,500,967.7z M748.4,325L448,623.1L301.6,477.9c-4.4-4.3-11.4-4.3-15.8,0c-4.4,4.3-4.4,11.3,0,15.6l151.2,150c0.5,1.3,1.4,2.6,2.5,3.7c4.4,4.3,11.4,4.3,15.8,0l308.9-306.5c4.4-4.3,4.4-11.3,0-15.6C759.8,320.7,752.7,320.7,748.4,325z\"</g>\n\t\t</svg>\n\t\t\t\t\t\t</a>\n</div>\n";

			return container_div + name_section + progress_bar + success_icon + "</div>";
		}).join("");

		$("#drop").classList.add("hidden");
		$("footer").classList.add("hasFiles");
		$(".importar").classList.add("active");
		setTimeout(function () {
			$(".list-files").innerHTML = template;
		}, 1000);

		Object.keys(files).forEach(function (file) {
			var load = 2000 + file * 2000; // fake load
			setTimeout(function () {
				$(".file--" + file).querySelector(".progress").classList.remove("active");
				$(".file--" + file).querySelector(".done").classList.add("anim");
			}, load);
		});
	}

	// trigger input
	$("#triggerFile").addEventListener("click", function (evt) {
		evt.preventDefault();
		$("input[type=file]").click();
	});

	// drop events
	$("#drop").ondragleave = function (evt) {
		$("#drop").classList.remove("active");
		evt.preventDefault();
	};
	$("#drop").ondragover = $("#drop").ondragenter = function (evt) {
		$("#drop").classList.add("active");
		evt.preventDefault();
	};
	$("#drop").ondrop = function (evt) {
		$("input[type=file]").files = evt.dataTransfer.files;
		$("footer").classList.add("hasFiles");
		$("#drop").classList.remove("active");
		evt.preventDefault();
	};

	//upload more
	$(".importar").addEventListener("click", function () {
	});

	// input change
	$("input[type=file]").addEventListener("change", handleFileSelect);
}();
