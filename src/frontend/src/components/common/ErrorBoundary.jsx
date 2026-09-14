import React from "react";
import { Component } from "react";
import PropTypes from "prop-types";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    console.error("CampusOS crashed:", error, info);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="w-full min-h-screen flex items-center justify-center bg-paper px-6">
          <div className="max-w-[420px] w-full bg-white border border-hairline rounded-sm p-8 text-center">
            <div className="font-serif text-[22px] font-bold text-ink mb-2">
              Something went wrong
            </div>
            <p className="text-[13.5px] text-slate mb-1">
              A part of the page hit an unexpected error. The rest of your session data is safe.
            </p>
            {this.state.error?.message && (
              <p className="font-mono text-[11px] text-urgent bg-urgent/10 rounded-sm px-3 py-2 my-4">
                {this.state.error.message}
              </p>
            )}
            <button
              onClick={() => { this.handleReset(); window.location.href = "/dashboard"; }}
              className="mt-3 rounded-sm py-2 px-5 text-[13px] font-medium text-white bg-[#1B2430] hover:bg-urgent transition-colors"
            >
              Back to dashboard
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

ErrorBoundary.propTypes = {
  children: PropTypes.node.isRequired,
};
