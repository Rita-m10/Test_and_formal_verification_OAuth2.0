#define Int_success (Int_knows == true);

mtype = {msg,
	id,                 /*идентификационный номер клиента*/
	Access_token, 
	Redirect_URI,       /*URI перенаправления*/
	Intruder_URI        /*URI злоумышленника*/
	Scope,              /*область применения*/
	State,              /*состояние*/
	Code,               /*код авторизации*/
	Error_description,  
	Responce_type,         
	Bearer,             /*тип токена*/
	Expires_in,         /*время жизни*/
	Access_scope
	ok,
	error,
	Source              /*запрошенный ресурс*/
}           

bool Int_knows = false;

/*код аутентификации*/
typedef AuthCode{      
	mtype client_id, uri, scope, code;
}

/*токен доступа*/
typedef AccessToken{   
	mtype c, uri, /*c-код авторизации, uri-URI-перенаправления*/ 
	token, type, time, scope;
}

/*доступ к ресурсам*/
typedef AccessSource{  
	mtype token, time, scope, source, status;
}

chan ClientUA = [0] of {mtype, AuthCode};  //Client - User Agent
chan UAAS = [0] of {mtype, AuthCode};      //User Agent - Avtorization server
chan token = [0] of {mtype, AccessToken}; 
chan resource = [0] of {mtype, AccessSource};
chan ErrorURI = [0] of {mtype};
chan toInt = [0] of {mtype, AuthCode};


//Клиент
active proctype Client(){
	//request - запрос, answer - ответ 
	AuthCode requestAC, answerAC; //AC - authorization code
	//Формируем сообщение-запрос на выдачу кода авторизации
	d_step{
		requestAC.client_id = id;
		requestAC.uri = Redirect_URI;
		requestAC.scope = Scope;
		requestAC.code = 0;
	}
	//Отправляем запрос на получение кода авторизации через user-agent
	ClientUA ! msg(requestAC);
	
	//Получаем ответ от user-agent (код авторизации)(или от Intruder)
	ClientUA ? msg(answerAC);
	
	AccessToken requestAT, answerAT; //AT - access token
	//Формируем сообщение-запрос на получение токена доступа
	d_step{
		requestAT.c = answerAC.code;
		requestAT.uri = answerAC.uri;
		requestAT.token = 0;
		requestAT.type = 0;
		requestAT.time = 0;
		requestAT.scope = answerAC.scope;
	}
	//Отправляем запрос серверу авторизации
	token ! msg(requestAT);
	
	//Получаем ответ от сервера авторизации (токен доступа)
	token ? msg(answerAT);
	
	AccessSource requestS, answerS;
	
	//Формируем запрос на получение данных 
	d_step{
		requestS.token = answerAT.token;
		requestS.time = answerAT.time;
		requestS.scope = answerAT.scope;
		requestS.source = 0;
		requestS.status = ok;
	}
	
	//Отправляем запрос серверу ресурсов
	resource ! msg(requestS);
	
	//Получаем запрошенные данные
	resource ? msg(answerS);
}

//Браузер
active proctype UserAgent(){
	AuthCode requestAC, answerAC;
	//Получаем запрос кода авторизации от клиента к серверу авторизации
	ClientUA ? msg(requestAC);  
	
	mtype IntURI;
	//Получаем URI злоумышленника
	ErrorURI ? IntURI; 
	
	mtype URI;
	//Недетерминированный выбор URI-перенаправления для симуляции разных случаев развития событий
	if 
	:: URI = requestAC.uri
	:: URI = IntURI
	fi
	
	requestAC.uri = URI;
	
	//Отправляем запрос серверу авторизации
	UAAS ! msg(requestAC);
	
	//Получаем ответ от сервера авторизации
	UAAS ? msg(answerAC);
	
	//Перенаправляем ответ по URI-перенаправления
	if
	:: (answerAC.uri == IntURI) 
		-> toInt ! msg(answerAC)
	:: else 
		-> ClientUA ! msg(answerAC)
	fi
}


//Сервер авторизации
active proctype Avtorization_server(){
	
	AuthCode requestAC, answerAC;
	//Получаем запрос от user-agent на получение кода авторизации
	UAAS ? msg(requestAC);
	//Формируем ответ
	d_step{
		answerAC.client_id = requestAC.client_id;
		answerAC.uri = requestAC.uri;
		answerAC.scope = requestAC.scope;
		answerAC.code = Code;
	}
	//Отправляем сообщение с кодом авторизации user-agent
	UAAS ! msg(answerAC);
	
	AccessToken answerAT, requestAT;
	
	//Получаем запрос на получение токена доступа от клиента
	token ? msg(requestAT);
	
	//Формируем ответ
	d_step{
		answerAT.c = requestAT.c;
		answerAT.uri = requestAT.uri;
		answerAT.token = Access_token;
		answerAT.type = Bearer;
		answerAT.time = Expires_in;
		answerAT.scope = Access_scope;
	}
	
	//Отправляем ответ с токеном клиенту
	token ! msg(answerAT);
}

active proctype Resource_server(){
	AccessSource requestS, answerS;
	
	resource ? msg(requestS);
	if
	:: (requestS.time != 0 && requestS.scope != 0 && requestS.token != 0) -> 
		d_step{
			answerS.token = requestS.token;
			answerS.time = requestS.time;
			answerS.scope = requestS.scope;
			answerS.source = Source;
			answerS.status = ok;
		}
	:: else -> 
		d_step{
			answerS.token = requestS.token;
			answerS.time = requestS.time;
			answerS.scope = requestS.scope;
			answerS.source = 0;
			answerS.status = error;
		}
	fi;
	
	resource ! msg(answerS);
}
 
active proctype Intruder(){
	mtype IntURI;
	IntURI = Intruder_URI;
	ErrorURI ! IntURI;
	
	
	AuthCode answerAC;
	toInt ? msg(answerAC);
	if 
	:: (answerAC.code != 0) -> Int_knows = true
	fi;
	ClientUA ! msg(answerAC);
	
	
}

ltl f {! <> Int_success}
