
export class API {
  constructor() {
    this.endpoint = "http://localhost:5000";
  }

  getVideoList(sinceId=null, untilId=null, count=null) {
    return axios.get(this.endpoint + "/api/videolist")
      .then((response) => {
        return Promise.resolve(response.data);
      });
  }

  getVideoListSince(sinceId=null, count=null) {
    let params = {};
    if( sinceId !== null ) params["since_id"] = sinceId;
    if( count !== null ) params["count"] = count;

    return axios.request({
        method: "get",
        url: this.endpoint + "/api/videolist-since",
        params: params
      }).then((response) => {
        return Promise.resolve(response.data);
      });
  }

  getVideoListUntil(untilId=null, count=null) {
    let params = {};
    if( untilId !== null ) params["until_id"] = untilId;
    if( count !== null ) params["count"] = count;

    return axios.request({
        method: "get",
        url: this.endpoint + "/api/videolist-until",
        params: params
      }).then((response) => {
        return Promise.resolve(response.data);
      });
  }

  getConfig(key) {
    return axios.request({
      method: "get",
      url: this.endpoint + "/api/config/" + key
    }).then((response) => {
      return Promise.resolve(response.data);
    });
  }

  setConfig(key, value) {
    let params = new URLSearchParams();
    params.append("value", value);

    return axios.request({
      method: "post",
      url: this.endpoint + "/api/config/" + key,
      data: params
    }).then((response) => {
      return Promise.resolve(response.data);
    });
  }

}
