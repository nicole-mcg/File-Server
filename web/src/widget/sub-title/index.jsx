import React from 'react';
import PropTypes from 'prop-types';

import './index.less'

import {cls} from "../../util/"

export default class SubTitle extends React.Component {
displayName: "SubTitle";
  render() {
    return (
        <div
            className={cls(this, "") + " " + this.props.className}
            style={this.props.style}>
            {this.props.children}
        </div>
    );
  }
}

SubTitle.propTypes = {
    className: PropTypes.string,
};

SubTitle.defaultProps = {
    className: "",
}