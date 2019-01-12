import React, { Component } from 'react';
import { Menu, Icon, Button } from 'antd';
import {Link } from 'react-router-dom';
import './HeadBar.css';
import Cookies from 'universal-cookie'

var cookies = new Cookies();

class Head extends React.Component {
    constructor(props) {
        super(props)
        this.handleLogout = this.props.handleLogout
    }
    state = {
        login: 'null',
        userid: 'null',
        role: 'null',
    }
    handleClick = (e) => {
        console.log('click ', e);
        this.setState({
            current: e.key,
        });
    }

    render() {
        let role = cookies.get("role");
        if(cookies.get("login") !== "true"){
                return (
                    <div>
                        <Menu
                            classname = 'menu'
                            theme = 'light'
                            onClick={this.handleClick}
                            selectedKeys={[this.state.current]}
                            mode="horizontal"
                        >
                            <Menu.Item key="home">
                                <Link to={'/'}><Icon type="home" />首页</Link>
                            </Menu.Item>
                            <Menu.Item key="user">
                                <Link to={'/Login'}><Icon type="login" />登录</Link>
                            </Menu.Item>
                        </Menu></div>
                );
        }
        else {
            if (role[0] === "ROLE_ADMIN") {
                return (
                    <div>
                        <Menu
                            classname='menu'
                            theme='light'
                            onClick={this.handleClick}
                            selectedKeys={[this.state.current]}
                            mode="horizontal"
                        >
                            <Menu.Item key="home">
                                <Link to={'/'}><Icon type="home"/>首页</Link>
                            </Menu.Item>
                            <Menu.Item key="user">
                                <Link to={'/User'}><Icon type="user"/>用户</Link>
                            </Menu.Item>
                            <Menu.Item key="bookList">
                                <Link to={'/BookList'}><Icon type="book"/>书库</Link>
                            </Menu.Item>
                            <Menu.Item key="shopping-cart">
                                <Link to={'/Cart'}><Icon type="shopping-cart"/>购物车</Link>
                            </Menu.Item>
                            <Menu.Item key="manage">
                                <Link to={'/Admin'}><Icon type="setting"/>管理</Link>
                            </Menu.Item>
                            <Menu.Item key="logout">
                                <Icon type="logout"onClick={this.handleLogout}>注销</Icon>
                            </Menu.Item>
                        </Menu></div>
                );
            }
            else if (role[0] === "ROLE_USER") {
                return (
                    <div>
                        <Menu
                            classname='menu'
                            theme='light'
                            onClick={this.handleClick}
                            selectedKeys={[this.state.current]}
                            mode="horizontal"
                        >
                            <Menu.Item key="home">
                                <Link to={'/'}><Icon type="home"/>首页</Link>
                            </Menu.Item>
                            <Menu.Item key="user">
                                <Link to={'/User'}><Icon type="user"/>用户</Link>
                            </Menu.Item>
                            <Menu.Item key="bookList">
                                <Link to={'/BookList'}><Icon type="book"/>书库</Link>
                            </Menu.Item>
                            <Menu.Item key="shopping-cart">
                                <Link to={'/Cart'}><Icon type="shopping-cart"/>购物车</Link>
                            </Menu.Item>
                            <Menu.Item key="logout">
                                <Icon type="logout"onClick={this.handleLogout}>注销</Icon>
                            </Menu.Item>
                        </Menu></div>
                );
            }
        }

    }
}

export default Head;