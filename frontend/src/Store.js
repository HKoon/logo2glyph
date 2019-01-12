import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './HomePage/App';

import { Form } from 'antd';
import { Route, Switch, HashRouter} from 'react-router-dom';
import Head from './HomePage/HeadBar';
import Cookies from 'universal-cookie';

var cookies = new Cookies();


class Store extends React.Component {
    constructor(props) {
        super(props)
        if (cookies.get('JSESSIONID') === 'null') {
            cookies.remove("login")
            cookies.remove("userid")
            cookies.remove("role")
        }

        this.state = {
            login: cookies.get('login'),
            role: cookies.get('role'),
            userid: cookies.get('userid'),
        }
    }

    LoginSuccessHandler = (userid, role) => {
        cookies.set("login",true,{path : '/'});
        cookies.set("role",role,{path : '/'});
        cookies.set("userid",userid,{path : '/'});
        window.location.href = "http://localhost:3000"
        this.setState({userid: userid,
            role:role,
            login:true,
        })
    }

    handleLogout = () => {
        fetch("http://localhost:8080/api/logout",{
            method: 'get',
            credentials: 'include'
        })
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        login: 'null',
                        userid: 'null',
                        role: 'null'
                    });
                    cookies.remove("JSESSIONID")
                    cookies.remove("login")
                    cookies.remove("userid")
                    cookies.remove("role")
                    window.location.href = "/";
                },
                (error) => {
                    console.log(error)
                }
            )
    }

    render(){
        let login = this.state.login;
        let role = this.state.role;
        let userid = this.state.userid;
        return(
            <div>
                <Head login={login} role={role} username={userid} handleLogout = {this.handleLogout}/>
                <Switch>
                    <Route exact path='/' component={App} />
                </Switch>
            </div>
        )
    }
}

export default Store