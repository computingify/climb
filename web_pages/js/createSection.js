export default createSection

function createSection(id) {
    const sec = document.createElement('section');
    sec.id = id;
    document.body.append(sec);
    return sec;
}