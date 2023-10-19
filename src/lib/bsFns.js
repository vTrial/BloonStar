// get unix time based on n days
const nDaysAgo = (n) => {
  const nowTime = Math.floor(Date.now() / 1000) // Convert milliseconds to seconds
  const pastTime = nowTime - 86400 * n
  return pastTime
}

export default nDaysAgo
