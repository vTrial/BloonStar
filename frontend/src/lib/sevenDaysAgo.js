const nowTime = Math.floor(Date.now() / 1000) // Convert milliseconds to seconds
const pastTime = nowTime - 86400 * 7
export { pastTime }
