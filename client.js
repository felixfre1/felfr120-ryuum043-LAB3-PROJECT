// js
// general
// テストのためのコード↓

const html = document.documentElement;
const body = document.getElementsByTagName("body");
const popUp = document.getElementsByClassName("pop-up");
const popUpForLatLng = document.getElementsByClassName("pop-up-for-lat-lng");
const pageContent = document.getElementsByClassName("page-content");
const token = () => localStorage.getItem("token");
const viewInfo = () => localStorage.getItem("view");
const decideView = () => {
	if (viewInfo() == "profilePage") {
		document.getElementById("page-content").innerHTML =
			document.getElementById("profile-view").innerHTML;
		profileLogic();
	} else {
		//TODO: delete query parameter
		document.getElementById("page-content").innerHTML =
			document.getElementById("welcome-view").innerHTML;
		welcomeLogic();
	}
};

window.onload = () => {
	decideView();
};

const showPopUpMessage = (message) => {
	popUp[0].classList.remove("pop-up-none");
	popUp[0].innerText = message;
	setTimeout(() => {
		popUp[0].classList.add("pop-up-none");
	}, 1500);
};

const showPopUpMessageForLatLng = (message) => {
	popUpForLatLng[0].classList.remove("pop-up-none");
	popUpForLatLng[0].innerText = message;
	setTimeout(() => {
		popUpForLatLng[0].classList.add("pop-up-none");
	}, 1500);
};

const welcomeLogic = () => {
	body[0].classList.add("body-for-welcome");
	const signInForm = document.getElementById("sign-in-form");
	const signInEmail = document.getElementById("sign-in-email");
	const signInPassword = document.getElementById("sign-in-password");
	const signUpForm = document.getElementById("sign-up-form");
	const signUpFirstName = document.getElementById("first-name");
	const signUpFamilyName = document.getElementById("family-name");
	const signUpGender = document.getElementById("gender");
	const signUpCity = document.getElementById("city");
	const signUpCountry = document.getElementById("country");
	const signUpEmail = document.getElementById("sign-up-email");
	const signUpPassword = document.getElementById("sign-up-password");
	const signUpRepeatPSW = document.getElementById("sign-up-repeat-password");
	const goToProfileView = () => {
		localStorage.setItem("view", "profilePage");
		decideView();
	};

	const signInFormSubmit = (e) => {
		e = e || window.event;
		const request = new XMLHttpRequest();
		// Communication Processing
		const PostSignIn = () => {
			request.open("POST", "/sign-in", true);
			request.setRequestHeader(
				"Content-Type",
				"application/json;charset=UTF-8"
			);
			request.send(
				JSON.stringify({
					email: signInEmail.value,
					password: signInPassword.value,
				})
			);
		};
		PostSignIn();
		// Response
		request.onload = () => {
			const res = JSON.parse(request.response);
			if (res.success) {
				localStorage.setItem("token", res.data.new_token);
				localStorage.setItem("userEmail", signInEmail.value);
				localStorage.setItem("userInfo", JSON.stringify(res.data.user_info));
				signInEmail.value = "";
				signInPassword.value = "";
				goToProfileView();
			} else showPopUpMessage(res.message);
		};
		e.preventDefault();
	};

	if (signInForm.addEventListener)
		signInForm.addEventListener("submit", signInFormSubmit, false);
	else signInForm.attachEvent("onsubmit", signInFormSubmit);

	const isDifferentPassword = () =>
		signUpPassword.value !== signUpRepeatPSW.value;

	const signUpFormSubmit = (e) => {
		e = e || window.event;
		if (signUpPassword.value.length <= 5)
			signUpPassword.setCustomValidity("Enter at least 6 characters");
		else if (signUpRepeatPSW.value.length <= 5)
			signUpRepeatPSW.setCustomValidity("Enter at least 6 characters");
		else if (isDifferentPassword())
			signUpRepeatPSW.setCustomValidity("Enter same password");
		else {
			const userInfo = {
				email: signUpEmail.value,
				firstname: signUpFirstName.value,
				familyname: signUpFamilyName.value,
				gender: signUpGender.value,
				city: signUpCity.value,
				country: signUpCountry.value,
			};
			const request = new XMLHttpRequest();
			// Communication Processing
			const PostSignUp = () => {
				request.open("POST", "/sign-up", true);
				request.setRequestHeader(
					"Content-Type",
					"application/json;charset=UTF-8"
				);
				const fullUserInfo = {
					email: signUpEmail.value,
					firstname: signUpFirstName.value,
					familyname: signUpFamilyName.value,
					gender: signUpGender.value,
					city: signUpCity.value,
					country: signUpCountry.value,
					password: signUpPassword.value,
				};
				request.send(JSON.stringify(fullUserInfo));
			};
			PostSignUp();
			// Response
			request.onload = () => {
				const res = JSON.parse(request.response);
				if (res.success) {
					localStorage.setItem("userInfo", JSON.stringify(userInfo));
					localStorage.setItem("userEmail", userInfo.email);
					localStorage.setItem("token", res.data);
					signUpEmail.value = "";
					signUpPassword.value = "";
					signUpFirstName.value = "";
					signUpFamilyName.value = "";
					signUpGender.value = "";
					signUpCity.value = "";
					signUpCountry.value = "";
					signUpRepeatPSW.value = "";
					goToProfileView();
				} else showPopUpMessage(res.message);
			};
		}
		e.preventDefault();
	};
	if (signUpForm.addEventListener)
		signUpForm.addEventListener("submit", signUpFormSubmit, false);
	else signUpForm.attachEvent("onsubmit", signUpFormSubmit);
};

const profileLogic = () => {
	body[0].classList.remove("body-for-welcome");
	const tabContent = document.getElementsByClassName("tab-content");
	const homeInputMessage = document.getElementById("home-input-message");
	const homePostButton = document.getElementById("home-post-button");
	const homeMessageList = document.getElementById("home-message-list");
	const homeReloadButton = document.getElementById("home-reload-button");
	const homeUserInfoHTML = document.querySelectorAll(".home-user-info text");
	const browseSearchedUserInfoHTML = document.querySelectorAll(
		".browse-user-info text"
	);
	const browseSearchInputEmail = document.getElementById("search-input-email");
	const browseSearchButton = document.getElementById("search-button");
	const browseInputMessage = document.getElementById("browse-input-message");
	const browsePostButton = document.getElementById("browse-post-button");
	const browseMessageList = document.getElementById("browse-message-list");
	const accountNewPassword = document.getElementById("new-password");
	const accountProfileRepeatPSW = document.getElementById("repeat-password");
	const accountOldPassword = document.getElementById("old-password");
	const accountUpdatePasswordForm = document.getElementById("account-form");
	const accountSignOutButton = document.getElementById("sign-out-button");
	const latitude = document.getElementById("lat");
	const longitude = document.getElementById("lng");
	const socket = io();
	socket.on("connect", () => {
		socket.emit("my_event", { data: "I'm connected!" });
	});
	const leaveEmailGroup = (email) => {
		socket.emit("leave", {
			room: email,
		});
	};
	const disconnectSocket = () => socket.emit("disconnect_request");
	const leaveOnlyLatestUser = () => {
		const request = new XMLHttpRequest();
		// Communication Processing
		//FIXME:function name should be changed to proper one.
		const checkToken = () => {
			request.open("GET", "/leave-only-latest-user", true);
			request.setRequestHeader("token", token());
			request.send();
		};
		checkToken();
		//Response
		request.onload = () => {
			const res = JSON.parse(request.response);
			if (res.success) {
				const email = localStorage.getItem("userEmail");
				leaveEmailGroup(email);
				disconnectSocket();
				goToWelcomeView();
			} else {
				console.log("this user has proper token.");
				showPopUpMessage(res.message);
			}
		};
	};

	socket.on("my_response", (msg, cb) => {
		console.log(msg.count, msg.data);
		if (msg.data == "is_latest_user") {
			leaveOnlyLatestUser();
		}
		if (cb) cb();
	});

	const showPosition = (position) => {
		if (position && position.coords) {
			const location = {
				lat: position.coords.latitude,
				lng: position.coords.longitude,
			};
			latitude.innerText = position.coords.latitude;
			longitude.innerText = position.coords.longitude;
			showPopUpMessageForLatLng("your location is loaded");
			return location;
		} else return false;
	};
	const getLocation = () => {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(showPosition);
		} else showPopUpMessage("Geolocation is not supported by this browser.");
	};
	getLocation();

	const goToWelcomeView = () => {
		localStorage.setItem("view", "welcomePage");
		decideView();
	};

	//いらないかも
	const addQueryParameter = () => {
		const url = new URL(window.location.href);
		const userInfo = JSON.parse(localStorage.getItem("userInfo"));
		if (!url.searchParams.get("email")) {
			url.searchParams.append("email", userInfo["email"]);
			location.href = url;
		} else if (!url.searchParams.get("firstname")) {
			url.searchParams.append("firstname", userInfo["firstname"]);
			location.href = url;
		} else if (!url.searchParams.get("familyname")) {
			url.searchParams.append("familyname", userInfo["familyname"]);
			location.href = url;
		} else if (!url.searchParams.get("city")) {
			url.searchParams.append("city", userInfo["city"]);
			location.href = url;
		} else if (!url.searchParams.get("country")) {
			url.searchParams.append("country", userInfo["country"]);
			location.href = url;
		} else if (!url.searchParams.get("gender")) {
			url.searchParams.append("gender", userInfo["gender"]);
			location.href = url;
		}
	};
	addQueryParameter();

	const joinEmailGroup = () => {
		const email = localStorage.getItem("userEmail");
		socket.emit("join", {
			room: email,
		});
	};
	joinEmailGroup();
	const sendMessageToEmailGroup = () => {
		const email = localStorage.getItem("userEmail");
		socket.emit("my_room_event", {
			room: email,
			data: "is_latest_user",
		});
	};
	sendMessageToEmailGroup();
	const homeUserDataInfo = () => {
		const request = new XMLHttpRequest();
		// Communication Processing
		const fetchHomeUserInfo = () => {
			request.open("GET", "/get-user-data-by-token", true);
			request.setRequestHeader("token", token());
			request.send();
		};
		fetchHomeUserInfo();
		//Response
		request.onload = () => {
			const res = JSON.parse(request.response);
			if (res.success) {
				localStorage.setItem("userInfo", JSON.stringify(res.data));
				for (let i = 0; i < homeUserInfoHTML.length; i++) {
					const className = homeUserInfoHTML[i].className;
					homeUserInfoHTML[i].innerText = res.data[className];
				}
			} else showPopUpMessage(res.message);
		};
	};
	homeUserDataInfo();

	const homeMessageInfo = () => {
		const request = new XMLHttpRequest();
		// Communication Processing
		const fetchHomeMessageInfo = () => {
			const email = localStorage.getItem("userEmail");
			request.open("GET", `/get-user-messages-by-email/${email}`, true);
			request.setRequestHeader("token", token());
			request.send();
		};
		fetchHomeMessageInfo();
		//Response
		request.onload = () => {
			const res = JSON.parse(request.response);
			if (res.success) {
				const list = [];
				for (let i = 0; i < res.data.length; i++) {
					list.push(
						`<text id="writer">${res.data[i].writer}</text>:  <text id="content"  draggable="true"
						>${res.data[i].content}</text>, <text>${res.data[i].city}</text>, <text>${res.data[i].country}</text><br/>`
					);
				}
				homeInputMessage.value = "";
				homeMessageList.innerHTML = list;
				homeMessageList.innerHTML = homeMessageList.innerHTML.replace(/,/g, "");
				tabContent[0].style.height = html.scrollHeight + "px";
				const homeMessageListChildren = homeMessageList.children;
				const textList = [];
				for (let i = 0; i < homeMessageListChildren.length; i++) {
					if (homeMessageListChildren[i].id === "content") {
						textList.push(homeMessageListChildren[i]);
					}
				}
				textList.map((textEle) => {
					textEle.ondragstart = (event) => {
						event.dataTransfer.setData("text", event.target.innerText);
					};
				});
			} else {
				showPopUpMessage(res.message);
				//TODO:should change logic
				// goToWelcomeView();
			}
		};
	};
	homeMessageInfo();

	homePostButton.onclick = () => {
		if (homeInputMessage.value) {
			const request = new XMLHttpRequest();
			// // Communication Processing
			const postMessageInfo = () => {
				const email = localStorage.getItem("userEmail");
				if (latitude.innerText && longitude.innerText) {
					request.open("POST", "/post-message", true);
					request.setRequestHeader("token", token());
					request.setRequestHeader(
						"Content-Type",
						"application/json;charset=UTF-8"
					);
					request.send(
						JSON.stringify({
							email: email,
							message: homeInputMessage.value,
							lat: latitude.innerText,
							lng: longitude.innerText,
						})
					);
				} else {
					showPopUpMessage("wait until server gets your location");
				}
			};
			postMessageInfo();
			// // Response
			request.onload = () => {
				const res = JSON.parse(request.response);
				
				if (res.success) {
					homeInputMessage.value = "";
					homeMessageInfo();
				} else showPopUpMessage(res.message);
			};
		}
	};

	homeReloadButton.onclick = () => {
		homeMessageInfo();
	};

	const browseSearchedUserInfo = (searchedUserEmail) => {
		const request = new XMLHttpRequest();
		// Communication Processing
		const fetchBrowseSearchedUserInfo = () => {
			request.open("GET", `/get-user-data-by-email/${searchedUserEmail}`, true);
			request.setRequestHeader("token", token());
			request.send();
		};
		fetchBrowseSearchedUserInfo();
		//Response
		request.onload = () => {
			const res = JSON.parse(request.response);
			if (res.success) {
				for (let i = 0; i < homeUserInfoHTML.length; i++) {
					const className = homeUserInfoHTML[i].className;
					browseSearchedUserInfoHTML[i].innerText = res.data[className];
				}
			} else showPopUpMessage(res.message);
		};
	};

	const browseSearchedUserMessage = (searchedUserEmail) => {
		const request = new XMLHttpRequest();
		// Communication Processing
		const fetchBrowseSearchedUserMessage = () => {
			request.open(
				"GET",
				`/get-user-messages-by-email/${searchedUserEmail}`,
				true
			);
			request.setRequestHeader("token", token());
			request.send();
		};
		fetchBrowseSearchedUserMessage();
		//Response
		request.onload = () => {
			const res = JSON.parse(request.response);
			if (res.success) {
				console.log(res);
				let list = [];
				for (let i = 0; i < res.data.length; i++) {
					list = res.data.map((data) => {
						return `<text id="writer">${data.writer}r</text>:  <text id="content">${data.content}</text>, <text>${res.data[i].city}</text>, <text>${res.data[i].country}</text><br/>`;
					});
				}
				browseMessageList.innerHTML = list;
				const replacedList = browseMessageList.innerHTML.replace(/,/g, "");
				browseMessageList.innerHTML = replacedList;
				tabContent[1].style.height = html.scrollHeight + "px";
			} else showPopUpMessage(res.message);
		};
	};

	const sendMessage = () => {
		if (browseSearchedUserInfoHTML[0].innerText !== "") {
			const searchedUserEmail = localStorage.getItem("searchedUserEmail");
			const request = new XMLHttpRequest();
			// Communication Processing
			const postMessage = () => {
				if (latitude.innerText && longitude.innerText) {
					request.open("POST", `/post-message`, true);
					request.setRequestHeader(
						"Content-Type",
						"application/json;charset=UTF-8"
					);
					request.setRequestHeader("token", token());
					request.send(
						JSON.stringify({
							message: browseInputMessage.value,
							email: searchedUserEmail,
							lat: latitude.innerText,
							lng: longitude.innerText,
						})
					);
				}
			};
			postMessage();
			//Response
			request.onload = () => {
				const res = JSON.parse(request.response);
				if (res.success) {
					browseSearchedUserMessage(searchedUserEmail);
					browseInputMessage.value = "";
					tabContent[1].style.height = html.scrollHeight + "px";
				} else showPopUpMessage(res.message);
			};
		} else showPopUpMessage("Search user first");
	};
	browseSearchButton.onclick = () => {
		const searchedUserEmail = browseSearchInputEmail.value;
		localStorage.setItem("searchedUserEmail", browseSearchInputEmail.value);
		browseSearchedUserInfo(searchedUserEmail);
		browseSearchedUserMessage(searchedUserEmail);
		browseSearchInputEmail.value = "";
	};

	browsePostButton.onclick = () => sendMessage();

	const profileIsDifferentPassword = () => {
		return accountNewPassword.value != accountProfileRepeatPSW.value;
	};
	const updatePassword = (e) => {
		e = e || window.event;
		if (accountNewPassword.value.length <= 5)
			accountNewPassword.setCustomValidity("Enter at least 6 characters");
		else if (accountProfileRepeatPSW.value.length <= 5)
			accountProfileRepeatPSW.setCustomValidity("Enter at least 6 characters");
		else if (accountOldPassword.value.length <= 5)
			accountOldPassword.setCustomValidity("Enter at least 6 characters");
		else if (profileIsDifferentPassword())
			accountProfileRepeatPSW.setCustomValidity("Enter same password");
		else {
			const request = new XMLHttpRequest();
			// Communication Processing
			const postChangePassword = () => {
				request.open("PUT", "/change-password", true);
				request.setRequestHeader("token", token());
				request.setRequestHeader(
					"Content-Type",
					"application/json;charset=UTF-8"
				);
				request.send(
					JSON.stringify({
						old_password: accountOldPassword.value,
						new_password: accountNewPassword.value,
					})
				);
			};
			postChangePassword();

			// Response
			request.onload = () => {
				const res = JSON.parse(request.response);
				if (res.success) {
					goToWelcomeView();
					accountOldPassword.value = "";
					accountProfileRepeatPSW.value = "";
					accountNewPassword.value = "";
				} else showPopUpMessage(res.message);
			};
		}
		e.preventDefault();
	};

	accountSignOutButton.onclick = () => {
		const request = new XMLHttpRequest();
		// Communication Processing
		const postSignOut = () => {
			request.open("POST", "/sign-out", true);
			request.setRequestHeader("token", token());
			request.send();
		};
		postSignOut();
		// Response
		request.onload = () => {
			const res = JSON.parse(request.response);
			if (res.success) {
				const email = localStorage.getItem("userEmail");
				leaveEmailGroup(email);
				disconnectSocket();
				goToWelcomeView();
			} else showPopUpMessage(res.message);
		};
	};

	if (accountUpdatePasswordForm.addEventListener)
		accountUpdatePasswordForm.addEventListener("submit", updatePassword, false);
	else accountUpdatePasswordForm.attachEvent("onsubmit", updatePassword);
};

// localStorage.setItem("view", "welcomePage");
