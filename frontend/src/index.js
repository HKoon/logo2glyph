import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './HomePage/App';

import Store from './Store.js'
import { Route, Switch, HashRouter} from 'react-router-dom';

ReactDOM.render(
    (
        <HashRouter>
            <Store />
        </HashRouter>
    ),
    document.getElementById("root")
);