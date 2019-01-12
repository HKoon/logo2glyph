import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Card, Icon, Avatar, Button, Upload, Modal, Input, Select } from 'antd';
import {Link } from 'react-router-dom';
import Cropper from 'react-cropper'
import 'cropperjs/dist/cropper.css'

const { Meta } = Card;
const Search = Input.Search;
const Option = Select.Option;


class App extends Component {

    constructor(props) {
        super(props);
        this.cropImage = this.cropImage.bind(this);
        this.state = {
            hasLoaded: false,
            isLoading: false,
            choicePicNum: 1,
            resPic: "",
            previewVisible: false,
            previewImage: '',
            fileList: [],
            nameList: [],
            title1:"",
            title2:""
        };
    }

    handleCancel = () => this.setState({ previewVisible: false })

    handlePreview = (file) => {
        console.log(this.state.fileList);
      this.setState({
        previewImage: file.url || file.thumbUrl,
        previewVisible: true,
      });
    }
    
    handleChange = ({ fileList }) => {
        this.setState({ fileList })
    }

    cropImage() {
        if (this.cropper.getCroppedCanvas() === 'null') {
            return false
        }
        this.props.getCropData(this.cropper.getCroppedCanvas().toDataURL())
    }

    handleChoiceChange= (value) => {
        console.log(value);
        var n = parseInt(value);
        console.log(value);
        this.setState({choicePicNum: n});
        console.log(this.state.choicePicNum);
      }

    handleSwitch(value){
        value = value.toUpperCase();
        this.setState({ isLoading: true });
        console.log(this.state.choicePicNum);
        console.log(value);
        let msg = "typepicname="+ encodeURIComponent(this.state.fileList[this.state.choicePicNum-1]['originFileObj']['name']) +
            "&content="+ encodeURIComponent(value)
        fetch("http://localhost:8080/api/switch", {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
            },
            body: msg
        })
        .then(
            res => res.json()
        )
        .then(
            (result) => {
                console.log(result)
                this.setState({resPic: "data:image/png;base64,"+result[0]['pic'],
                cmpPic: "data:image/png;base64,"+result[1]['cmp'],
                isLoading: false,
                hasLoaded: true,
                title1:"转换结果",
                title2:"对比图"
            })
            }
        )
    }

    
  render() {
    const { previewVisible, previewImage, fileList } = this.state;
    const uploadButton = (
        <div>
          <Icon type="plus" />
          <div className="ant-upload-text">Upload</div>
        </div>
      );
    return (
        
      <div className="App">

          <div>
            <header className="App-header">
              <h1 className = "title">Font Switch |字体转换</h1>
              <h1 className="App-title">字体转换</h1>
              <img src={logo} className="App-logo" alt="logo"/>
            </header>
          </div>
        <br></br>

        <div className="uploadStyle">
            <h2 className="upload-title">上传字体风格</h2>
            <div className="upload">
            <Upload
                action="//jsonplaceholder.typicode.com/posts/"
                listType="picture-card"
                fileList={fileList}
                onPreview={this.handlePreview}
                onChange={this.handleChange}
            >
            {fileList.length >= 3 ? null : uploadButton}
            </Upload>
            </div>
            <Modal visible={previewVisible} footer={null} onCancel={this.handleCancel}>
            <img alt="example" style={{ width: '100%' }} src={previewImage} />
            </Modal>
        </div>
        <br></br>

        <div>
            <h2 className="choice-title">选择字体风格</h2>
            <Select defaultValue="Style 1" style={{ width: 120 }} onChange={this.handleChoiceChange}>
            <Option value="1">Style 1</Option>
            <Option value="2">Style 2</Option>
            <Option value="3" disabled>Style 3</Option>
            <Option value="4">Style 4</Option>
            </Select>
        </div>
        <br></br>

        <div className="content">
            <h2 className="input_content">输入文本</h2>
            <Search
            placeholder="input text"
            enterButton="Switch!"
            size="large"
            onSearch={value => this.handleSwitch(value)}
            />
        </div>
        <br></br>
        <div>
{ this.state.hasLoaded ?
        <div>
            <h2 style={{float:"left",marginLeft:"15%"}}>转换结果</h2>
            <h2 style={{float:"right",marginRight:"32%"}}>对比图</h2>
            <br></br>
        </div>
        :
        <div></div>
}
        </div>

        <div>
            { this.state.isLoading ?
                <Icon type="loading" style={{fontSize:100}}/>
            :
                <div>
                    <img src={this.state.resPic} style={{float:"left",marginLeft:"0%"}} className="cmpImage"/>
                    <img src={this.state.cmpPic} style={{float:"right",marginRight:"0%"}} className="resImage"/>
                </div>
            }
            <br></br>
        </div>
        <br></br>
      </div>
    );
  }
}

export default App;
